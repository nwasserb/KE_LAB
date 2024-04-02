import pyvisa as visa
import time
from time import sleep
import pandas as pd
import random
import os

def initialize_devices():
    resourceManager = visa.ResourceManager()
    
    # Initialize main device
    dev = 'TCPIP0::10.0.3.17::5000::SOCKET'
    session = resourceManager.open_resource(dev)
    print('\nMain device open successful!')
    session.read_termination = '\n'
    session.write_termination = '\n'
    
    # Initialize EPC_prep device
    EPC_prep = 'ASRL15::INSTR'
    session_EPC_prep = resourceManager.open_resource(EPC_prep)
    print('\nEPC_prep device open successful!')
    session_EPC_prep.baud_rate = 9600
    session_EPC_prep.read_termination = None
    session_EPC_prep.write_termination = '\r\n'
    session_EPC_prep.query_termination = '\r\n'
    
    # Initialize EPC device
    EPC = 'ASRL3::INSTR'
    session_EPC = resourceManager.open_resource(EPC)
    print('\nEPC device open successful!')
    session_EPC.baud_rate = 9600
    session_EPC.read_termination = None
    session_EPC.write_termination = '\r\n'
    session_EPC.query_termination = '\r\n'
    
    return session, session_EPC_prep, session_EPC

def read_data(session, relPort1mW, relPort2mW, relPort3mW, relPort4mW):
    sleep(0.05)
    result = session.query('READ? 0')
    ports = result.split(',')
    port1 = float(ports[0].split(':')[-1])
    port2 = float(ports[1])
    port3 = float(ports[2])
    port4 = float(ports[3])

    port1mW = float(pow(10, port1 / 10))
    port2mW = float(pow(10, port2 / 10))
    port3mW = float(pow(10, port3 / 10))
    port4mW = float(pow(10, port4 / 10))

    totalmW = port1mW + port2mW + port3mW + port4mW

    relPort1mW.append(port1mW / totalmW)
    relPort2mW.append(port2mW / totalmW)
    relPort3mW.append(port3mW / totalmW)
    relPort4mW.append(port4mW / totalmW)

def run_sequence(session, session_EPC_prep, relPort1mW, relPort2mW, relPort3mW, relPort4mW, variable_sleep):
    for _ in range(100):
        read_data(session, relPort1mW, relPort2mW, relPort3mW, relPort4mW)

    t_end = time.time() + 60 * 1 
    while time.time() < t_end:
        v_digit = random.randint(1, 4)
        random_number = random.randint(-5000, 5000)
        query_string = f"V{v_digit},{random_number}"
        zero_query_string = f"V{v_digit},0"
        session_EPC_prep.query(query_string)
        time.sleep(variable_sleep)  # Use variable sleep time here
        session_EPC_prep.query(zero_query_string)
        time.sleep(variable_sleep)  # Use variable sleep time here
        read_data(session, relPort1mW, relPort2mW, relPort3mW, relPort4mW)
        print("Running")

    for _ in range(100):
        read_data(session, relPort1mW, relPort2mW, relPort3mW, relPort4mW)

def main():
    session, session_EPC_prep, session_EPC = initialize_devices()
    
    delays = [.05, .06, .07, .08, .09, .1, .15, .2, .25, .3, .35, .4, .5, .75, 1, 1.5, 2]
    # delays = [.005, .05]
    for i in delays:
        relPort1mW = []
        relPort2mW = []
        relPort3mW = []
        relPort4mW = []

        run_sequence(session, session_EPC_prep, relPort1mW, relPort2mW, relPort3mW, relPort4mW, i)

        # Create folder if it doesn't exist
        folder_path = "delay_csv"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_name = f"prep_state_data_{i}.csv"
        file_path = os.path.join(folder_path, file_name)

        data = pd.DataFrame({
            "port1_Relative_Power": relPort1mW,
            "port2_Relative_Power": relPort2mW,
            "port3_Relative_Power": relPort3mW,
            "port4_Relative_Power": relPort4mW,
        })

        data.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")

if __name__ == "__main__":
    main()
