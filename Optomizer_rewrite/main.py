#==================== Imports ====================
import pyvisa as visa
from threading import Thread, Event
import pandas as pd
from time import sleep

from epc_optimizer import EPCOptimizer

#==================== Function Definitions ====================
def print_detector_percent_values(epc_optimizer, event):
    while(not event.is_set()):
        ports_percent = epc_optimizer.read_detector_percent()

        output_list = []
        for i, port_percent in enumerate(ports_percent, 1):
            output_list.append(f"Port {i}: {port_percent:<+6.5f}%")

        print(" | ".join(output_list), end="\r")

def wait_for_input(event):
    while(True):
        user_input = input("Enter 'stop' to stop the loop: ")
        if user_input.lower() == "stop":
            event.set()
            break

def state_prep(epc_optimizer):
    input_diagonal_voltages = (0, 0, 0, 0)

    while(True):
        #Horizontal
        epc_optimizer.set_epc_stateprep(*epc_optimizer.horizontal_params)
        horizontal_ports_percent = epc_optimizer.read_detector_percent()
        print(f"Horizontal: {horizontal_ports_percent}")
        sleep(0.05)
        #Diagonal
        raw_input = input("Enter V1, V2, V3, V4 : ")
        if raw_input == "stop":
            return input_diagonal_voltages

        raw_input_diagonal_voltages = raw_input.split(",")
        input_diagonal_voltages = tuple(float(raw_input_diagonal_voltage) for raw_input_diagonal_voltage in raw_input_diagonal_voltages)
        epc_optimizer.set_epc_stateprep(*input_diagonal_voltages)
        sleep(0.05)
        diagonal_ports_percent = epc_optimizer.read_detector_percent()
        print(f"Diagonal: {diagonal_ports_percent}")

if __name__ == "__main__":
    #==================== STAGE 0: Initialize Code ====================
    #Initialize constants
    DETECTOR_RESOURCE_STR = "TCPIP0::10.0.3.17::5000::SOCKET"
    EPC_STATEPREP_RESOURCE_STR = "ASRL15::INSTR"
    EPC_FEEDBACK_RESOURCE_STR = "ASRL3::INSTR"
    OPTIMIZER_OPTIONS = {
        "maxiter": 500,
        # "learning_rate": 0.93,
        "learning_rate": 0.4,
        "perturbation": 2e-7
    }

    #Initialize PyVISA sessions
    resource_manager = visa.ResourceManager() #PyVISA Resource Manager
    detector_session                   = resource_manager.open_resource(DETECTOR_RESOURCE_STR)
    detector_session.read_termination  = "\n"
    detector_session.write_termination = "\n"

    #EPC for state preperation
    epc_stateprep_session                   = resource_manager.open_resource(EPC_STATEPREP_RESOURCE_STR)
    epc_stateprep_session.read_termination  = "\r\n"
    epc_stateprep_session.write_termination = "\r\n"
    epc_stateprep_session.query_termination = "\r\n"

    #EPC for optimizing
    epc_feedback_session                   = resource_manager.open_resource(EPC_FEEDBACK_RESOURCE_STR)
    epc_feedback_session.read_termination  = "\r\n"
    epc_feedback_session.write_termination = "\r\n"
    epc_feedback_session.query_termination = "\r\n"

    #Initialize EPC Optimizer and zero both EPCs
    epc_optimizer = EPCOptimizer(detector_session, epc_stateprep_session, epc_feedback_session, OPTIMIZER_OPTIONS)
    epc_optimizer.zero_epc_stateprep()
    epc_optimizer.zero_epc_feedback()

    #==================== STAGE 1: Initialize orthogonal states ====================
    init_event = Event()
    read_thread = Thread(target=print_detector_percent_values, args=(epc_optimizer, init_event))
    input_thread = Thread(target=wait_for_input, args=(init_event,))

    read_thread.start()
    input_thread.start()

    read_thread.join()
    input_thread.join()

    #==================== STAGE 2: State Preperation ====================
    diagonal_params = state_prep(epc_optimizer)
    epc_optimizer.set_diagonal_params(*diagonal_params)

    #==================== STAGE 3: Optimizing ====================
    epc_optimizer.run()

    #==================== STAGE 4: Export data ====================
    #Too lazy to rename all of these
    port1_mW_H_df = [ports[0] for ports in epc_optimizer.horizontal_power]
    port2_mW_H_df = [ports[1] for ports in epc_optimizer.horizontal_power]
    port3_mW_H_df = [ports[2] for ports in epc_optimizer.horizontal_power]
    port4_mW_H_df = [ports[3] for ports in epc_optimizer.horizontal_power]
    port1_mW_D_df = [ports[0] for ports in epc_optimizer.diagonal_power]
    port2_mW_D_df = [ports[1] for ports in epc_optimizer.diagonal_power]
    port3_mW_D_df = [ports[2] for ports in epc_optimizer.diagonal_power]
    port4_mW_D_df = [ports[3] for ports in epc_optimizer.diagonal_power]
    port1_V_df = [ports[0] for ports in epc_optimizer.input_params]
    port2_V_df = [ports[1] for ports in epc_optimizer.input_params]
    port3_V_df = [ports[2] for ports in epc_optimizer.input_params]
    port4_V_df = [ports[3] for ports in epc_optimizer.input_params]
    cost_val = epc_optimizer.cost

    data_HD = pd.DataFrame({
        "port1_H" : port1_mW_H_df,
        "port2_H" : port2_mW_H_df,
        "port3_H" : port3_mW_H_df,
        "port4_H" : port4_mW_H_df,
        "port1_D" : port1_mW_D_df,
        "port2_D" : port2_mW_D_df,
        "port3_D" : port3_mW_D_df,
        "port4_D" : port4_mW_D_df,
    })
    data_costV = pd.DataFrame({
        "V1"    : port1_V_df,
        "V2"    : port2_V_df,
        "V3"    : port3_V_df,
        "V4"    : port4_V_df,
        "Cost"  : cost_val
    })

    data_HD.to_csv('EPC_OPTO_SLEEP_HD.csv', index=False)
    data_costV.to_csv('EPC_OPTO_SLEEP_costV.csv', index=False)
