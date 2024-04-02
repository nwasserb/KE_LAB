import pyvisa as visa
import pandas as pd
import pulp
from time import sleep

# Read detector voltage values
def read_detector_power_values(detector_session):
    sleep(0.05)
    result = detector_session.query('READ? 0')
    ports = result.split(',')
    port1_mW = float(pow(10, float(ports[0].split(':')[-1])/10))
    port2_mW = float(pow(10, float(ports[1])/10))
    port3_mW = float(pow(10, float(ports[2])/10))
    port4_mW = float(pow(10, float(ports[3])/10))
    return [port1_mW, port2_mW, port3_mW, port4_mW]

# Objective function
def objective_function(detector_session):
    port1_mW, _, _, _ = read_detector_power_values(detector_session)
    return -(port1_mW)

# Write values to the device
def write_values_to_device(values, epc_session):
    # Write the values to the device
    for i, value in enumerate(values, start=1):
        epc_session.write(f'V{i},{int(value)}')

# Minimize with integer constraints
def minimize_with_integer_constraints(objective_function, initial_values, integer_indices, epc_session, detector_session):
    # Create LP problem
    prob = pulp.LpProblem("Integer Optimization", pulp.LpMinimize)

    # Define variables
    x_vars = [pulp.LpVariable(f'x_{i}', lowBound=-5000, upBound=5000, cat='Integer') if i in integer_indices else pulp.LpVariable(f'x_{i}', lowBound=-5000, upBound=5000) for i in range(4)]

    # Set initial values for variables
    for var, value in zip(x_vars, initial_values):
        var.setInitialValue(value)

    # Add objective function
    prob += objective_function(detector_session)

    # Solve the problem
    prob.solve()

    # Write optimized values to the device
    optimized_values = [pulp.value(var) for var in x_vars]
    write_values_to_device(optimized_values, epc_session)
    print("Volts: ", optimized_values)
    print("POWER: ", objective_function(detector_session))
    # Return the optimized values
    return objective_function(detector_session)

if __name__ == "__main__":
    # Initialize constants
    DETECTOR_RESOURCE_STR = "TCPIP0::10.0.0.2::5000::SOCKET"
    EPC_RESOURCE_STR = "ASRL3::INSTR"
    EPC_BOUNDS = (-5000, 5000)

    # Open PyVISA Sessions
    resource_manager = visa.ResourceManager() # PyVISA Resource Manager
    detector_session = resource_manager.open_resource(DETECTOR_RESOURCE_STR)
    detector_session.read_termination = "\n"
    detector_session.write_termination = "\n"

    epc_session = resource_manager.open_resource(EPC_RESOURCE_STR)
    epc_session.read_termination = "\r\n"
    epc_session.write_termination = "\r\n"
    epc_session.query_termination = "\r\n"

    try:
        # Set initial values and integer indices
        initial_values = [0, 0, 0, 0]
        integer_indices = [0, 1, 2, 3]  # All variables should be integers

        # Minimize with integer constraints
        result = minimize_with_integer_constraints(objective_function, initial_values, integer_indices, epc_session, detector_session)

    except visa.errors.VisaIOError:
        raise Exception("Retry script!, Weird VISA bug?")
