from qiskit_algorithms.optimizers import SPSA
import pyvisa as visa
import numpy as np
from time import sleep

def wrap_voltage(value, low=-5000, high=5000):
    if(value >= low and value <= high):
        return value
    else:
        return (-np.abs(value) % 5000) * np.sign(value)
    
    # diff = high - low
    # return (((value - low) % diff) + low)

class EPCOptimizer:
    def __init__(self, detector_session, epc_stateprep_session, epc_feedback_session, optimizer_options):
        self.epc_stateprep_session = epc_stateprep_session
        self.epc_feedback_session = epc_feedback_session
        self.detector_session = detector_session
        self.optimizer_options = optimizer_options

        self.SLEEP_TIME = 0.05
        self.EPC_BOUNDS = [(-5000.0, 5000.0), (-5000.0, 5000.0), (-5000.0, 5000.0), (-5000.0, 5000.0)]
        self.INIT_GUESS = (2000.0, 2000.0, 2000.0, 2000.0)
        self.horizontal_params = (0, 0, 0, 0)
        self.diagonal_params = None

        self.horizontal_power = []
        self.diagonal_power = []
        self.input_params = []
        self.cost = []

    def read_detector_dB(self):
        #Sleep to avoid reading transient behavior in EPC
        sleep(self.SLEEP_TIME)

        #Read detector voltage values
        result = self.detector_session.query("READ? 0")

        #Split the string based on the comma (",") separator
        ports = result.split(",")

        #Convert the strings to float numbers
        port1_dB = float(ports[0].split(":")[-1])
        port2_dB = float(ports[1])
        port3_dB = float(ports[2])
        port4_dB = float(ports[3])

        return (port1_dB, port2_dB, port3_dB, port4_dB)

    def read_detector_mW(self):
        ports_dB = self.read_detector_dB()
        ports_mW = tuple(float(pow(10, port_dB / 10)) for port_dB in ports_dB)

        return ports_mW

    def read_detector_percent(self):
        ports_mW = self.read_detector_mW()
        
        total_power = sum(ports_mW)
        ports_percent = tuple(port_mW / total_power for port_mW in ports_mW)

        return ports_percent

    def set_epc_stateprep(self, v1, v2, v3, v4):
        inp_voltages = (v1, v2, v3, v4)

        for i, inp_voltage in enumerate(inp_voltages, 1):
            sleep(self.SLEEP_TIME)
            # sleep(.01)      #HARD CODED VALUE FOR TESTING
            self.epc_stateprep_session.query(f"V{i},{int(inp_voltage)}")
        #sleep(self.SLEEP_TIME)

    def set_epc_feedback(self, v1, v2, v3, v4):
        inp_voltages = (v1, v2, v3, v4)

        for i, inp_voltage in enumerate(inp_voltages, 1):
            sleep(self.SLEEP_TIME)
            # sleep(.01)#HARD CODED VALUE FOR TESTING
            self.epc_feedback_session.query(f"V{i},{int(inp_voltage)}")
        #sleep(self.SLEEP_TIME)

    def zero_epc_stateprep(self):
        self.set_epc_stateprep(0, 0, 0, 0)

    def zero_epc_feedback(self):
        self.set_epc_feedback(0, 0, 0, 0)

    def set_diagonal_params(self, v1, v2, v3, v4):
        self.diagonal_params = (v1, v2, v3, v4)

    def __callback(self, func_evals, params, cost, step_size, step_accepted):
        #Query EPC voltages for optimizing
        wrapped_params = tuple(wrap_voltage(voltage) for voltage in params)
        self.set_epc_feedback(*wrapped_params)
        # self.set_epc_feedback(*params)

        #Update input_params and cost data
        self.input_params.append(wrapped_params)
        # self.input_params.append(params)
        self.cost.append(cost)

        #Measure horizontal state
        self.set_epc_stateprep(*self.horizontal_params)
        horizontal_ports_percent = self.read_detector_percent()
        self.horizontal_power.append(horizontal_ports_percent)

        #Measure diagonal state
        self.set_epc_stateprep(*self.diagonal_params)
        diagonal_ports_percent = self.read_detector_percent()
        self.diagonal_power.append(diagonal_ports_percent)

        #DEBUG
        print(f"{str(params):45}, {cost=:.5f}", end="\r")


    def __objective_function(self, params):
        #Send horizontal state and measure power
        self.set_epc_stateprep(*self.horizontal_params)
        horizontal_ports_percent = self.read_detector_percent()
        # self.horizontal_power.append(horizontal_ports_percent) #This might not be right

        #Send diagonal state and measure power
        self.set_epc_stateprep(*self.diagonal_params)
        diagonal_ports_percent = self.read_detector_percent()
        # self.diagonal_power.append(diagonal_ports_percent) #This might not be right

        #I'm too lazy to rename all of this
        H_port1_mW, H_port2_mW, H_port3_mW, H_port4_mW = horizontal_ports_percent
        D_port1_mW, D_port2_mW, D_port3_mW, D_port4_mW = diagonal_ports_percent
        return \
            (H_port1_mW - 0.50) ** 2 + (H_port2_mW) ** 2 + \
            (H_port3_mW - 0.25) ** 2 + (H_port4_mW - 0.25) ** 2 + \
            (D_port1_mW - 0.25) ** 2 + (D_port2_mW - 0.25) ** 2 + \
            (D_port3_mW - 0.50) ** 2 + (D_port4_mW) ** 2

    def run(self):
        self.optimizer_options["callback"] = self.__callback
        spsa = SPSA(**self.optimizer_options)

        try:
            result = spsa.minimize(
                self.__objective_function,
                x0=self.INIT_GUESS,
                bounds=self.EPC_BOUNDS)
        except visa.errors.VisaIOError:
            print("Caught VisaIOError. Retrying script...")
        