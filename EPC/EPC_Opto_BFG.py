import pyvisa as visa
from qiskit_algorithms.optimizers import SPSA
from time import sleep
import pandas as pd
from scipy.optimize import minimize


#Read detector voltage values
def read_detector_power_values(detector_session):
    sleep(0.05)
    result = detector_session.query('READ? 0')

    # Split the string based on the comma (',') separator
    ports = result.split(',')

    # Convert the strings to float numbers
    port1 = float(ports[0].split(':')[-1])
    port2 = float(ports[1])
    port3 = float(ports[2])
    port4 = float(ports[3])

    port1_mW = float(pow(10, port1/10))
    port2_mW = float(pow(10, port2/10))
    port3_mW = float(pow(10, port3/10))
    port4_mW = float(pow(10, port4/10))

    # total_mW = port1_mW + port2_mW + port3_mW + port4_mW

    # rel_port1_mW = port1_mW / total_mW
    # rel_port2_mW = port2_mW / total_mW
    # rel_port3_mW = port3_mW / total_mW
    # rel_Port4_mW = port4_mW / total_mW

    return [port1_mW, port2_mW, port3_mW, port4_mW]

def objective_function(params):
    port1_mW, port2_mW, port3_mW, port4_mW = read_detector_power_values(detector_session)

    rounded_params = [round(param) for param in params]



    epc_query_strings = [f"V{port},{int(inp_voltage)}" for port, inp_voltage in zip(range(1, len(rounded_params) + 1), rounded_params)]
    for epc_query_string in epc_query_strings:
        epc_session.query(epc_query_string)
    print(f"Optimization Step: {len(callback.steps)}")
    print(f"phi Values: {params}")
    #DEBUG
    # print(f"{port1_mW=}, {port2_mW=}, {port3_mW=}, {port4_mW=}", end="\r")

    #For maximize port 1 and minimize port 2 (Negative for minimizing)
    #return -((port1_mW) ** 2) + (port2_mW) ** 2
    # return -(port1_mW**2)
    return -((port1_mW) ** 2) + ((port3_mW-port4_mW) ** 2)
    # return -(port1_mW) + abs((port3_mW-port4_mW))

def callback(params):
    global port1_mW_df
    global port2_mW_df
    global port3_mW_df
    global port4_mW_df
    global port1_V_df
    global port2_V_df
    global port3_V_df
    global port4_V_df


    #DEBUG
    port1_mW, port2_mW, port3_mW, port4_mW = read_detector_power_values(detector_session)
    total_mW = port1_mW + port2_mW + port3_mW + port4_mW
    rel_port1_mW = port1_mW / total_mW

    callback.steps.append(rel_port1_mW)

    port1_mW_df.append(port1_mW)
    port2_mW_df.append(port2_mW)
    port3_mW_df.append(port3_mW)
    port4_mW_df.append(port4_mW)

    port1_V_df.append(params[0])
    port2_V_df.append(params[1])
    port3_V_df.append(params[2])
    port4_V_df.append(params[3])


callback.steps = []

port1_mW_df = []
port2_mW_df = []
port3_mW_df = []
port4_mW_df = []
port1_V_df = []
port2_V_df = []
port3_V_df = []
port4_V_df = []



if __name__ == "__main__":
    #Initialize constants
    DETECTOR_RESOURCE_STR = "TCPIP0::10.0.0.2::5000::SOCKET"
    EPC_RESOURCE_STR      = "ASRL3::INSTR"
    EPC_BOUNDS            = (-5000, 5000)
    LEARNING_RATE         = .25
    PERTURBATION          = 5e-4
    MAX_ITERATIONS        = 1000

    #Open PyVISA Sessions
    resource_manager = visa.ResourceManager() #PyVISA Resource Manager
    
    detector_session                   = resource_manager.open_resource(DETECTOR_RESOURCE_STR)
    detector_session.read_termination  = "\n"
    detector_session.write_termination = "\n"

    epc_session                   = resource_manager.open_resource(EPC_RESOURCE_STR)
    epc_session.read_termination  = "\r\n"
    epc_session.write_termination = "\r\n"
    epc_session.query_termination = "\r\n"

    #Perform SPSA Optimization
    initial_input_voltages = [0, 0, 0, 0] #Initial guess for input voltages

    # lambda_objective_function = lambda epc_voltage_values : objective_function(epc_voltage_values, detector_session)
    # lambda_callback           = lambda func_evals, params, cost, step_size, step_accepted : callback(func_evals, params, cost, step_size, step_accepted, epc_session)
    

    try:
        initial_phi_values = [3000, -2500, 3000, -2500]
        result = minimize(objective_function, initial_phi_values, method='BFGS', options={'disp': True, 'maxiter': 10000}, callback=callback)

        #DEBUG
        optimal_voltage_values = result.x
        final_cost             = result.fun
        num_of_func_evals      = result.nfev
        
        print(f"{optimal_voltage_values=}")
        print(f"{final_cost=}")
        print(f"{num_of_func_evals=}")
    except visa.errors.VisaIOError:
        raise Exception("Retry script!, Weird VISA bug?")

    #DEBUG
    final_detector_power_values = read_detector_power_values(detector_session)
    print(f"{final_detector_power_values=}")

    data = pd.DataFrame({
        "port1" : port1_mW_df,
        "port2" : port2_mW_df,
        "port3" : port3_mW_df,
        "port4" : port4_mW_df,
        "V1"    : port1_V_df,
        "V2"    : port2_V_df,
        "V3"    : port3_V_df,
        "V4"    : port4_V_df
    })
    data.to_csv('EPC_OPTO_SLEEP_.csv', index=False)  

