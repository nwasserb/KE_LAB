import pyvisa as visa
import time
import math
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import pandas as pd
import threading
import random

resourceManager = visa.ResourceManager()
dev = 'TCPIP0::10.0.3.17::5000::SOCKET'
session = resourceManager.open_resource(dev)
print('\n Open Successful!')
session.read_termination = '\n'
session.write_termination = '\n'

EPC_prep = 'ASRL15::INSTR'
session_EPC_prep = resourceManager.open_resource(EPC_prep)
print('\n Open Successful!')
session_EPC_prep.baud_rate = 9600
session_EPC_prep.read_termination = None
session_EPC_prep.write_termination = '\r\n'
session_EPC_prep.query_termination = '\r\n'

EPC = 'ASRL3::INSTR'
session_EPC = resourceManager.open_resource(EPC)
print('\n Open Successful!')
session_EPC.baud_rate = 9600
session_EPC.read_termination = None
session_EPC.write_termination = '\r\n'
session_EPC.query_termination = '\r\n'


session_EPC_prep.query('VZ1')
session_EPC_prep.query('VZ2')
session_EPC_prep.query('VZ3')
session_EPC_prep.query('VZ4')

session_EPC.query('VZ1')
session_EPC.query('VZ2')
session_EPC.query('VZ3')
session_EPC.query('VZ4')

def read_data(relPort1mW, relPort2mW, relPort3mW, relPort4mW):
    sleep(0.05)
    result = session.query('READ? 0')
    # Split the string based on the comma (',') separator
    ports = result.split(',')

    # Convert the strings to float numbers
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



# Lists to store relative powers
relPort1mW = []
relPort2mW = []
relPort3mW = []
relPort4mW = []

for n in range(1,100):
    read_data(relPort1mW, relPort2mW, relPort3mW, relPort4mW)

t_end = time.time() + 60 * 1 
while time.time() < t_end:

    # Generate random number for the digit after "V"
    v_digit = random.randint(1, 4)
    # Generate random number for the integer value
    random_number = random.randint(-5000, 5000)
    # Concatenate the strings
    query_string = f"V{v_digit},{random_number}"    
    zero_query_string = f"V{v_digit},0"
    # Jump from -5000 V to 0
    session_EPC_prep.query(query_string)
    sleep(0.05)

    # Jump from -5000 V to 0
    session_EPC_prep.query(zero_query_string)
    sleep(0.05)
    # Inside the while loop
    read_data(relPort1mW, relPort2mW, relPort3mW, relPort4mW)
    print("Running")


for n in range(1,100):
    read_data(relPort1mW, relPort2mW, relPort3mW, relPort4mW)

t_end = time.time() + 60 * 1 
while time.time() < t_end:

    # Generate random number for the digit after "V"
    v_digit = random.randint(1, 4)
    # Generate random number for the integer value
    random_number = random.randint(-5000, 5000)
    # Concatenate the strings
    query_string = f"V{v_digit},{random_number}"    
    zero_query_string = f"V{v_digit},0"
    # Jump from -5000 V to 0
    session_EPC_prep.query(query_string)
    sleep(0.05)

    # Jump from -5000 V to 0
    session_EPC_prep.query(zero_query_string)
    sleep(0.05)
    # Inside the while loop
    read_data(relPort1mW, relPort2mW, relPort3mW, relPort4mW)
    print("Running")

for n in range(1,100):
    read_data(relPort1mW, relPort2mW, relPort3mW, relPort4mW)


# Save data to CSV
data = pd.DataFrame({
    "port1_Relative_Power": relPort1mW,
    "port2_Relative_Power": relPort2mW,
    "port3_Relative_Power": relPort3mW,
    "port4_Relative_Power": relPort4mW,
})
print(data)
data.to_csv('Prep_state_data.csv', index=False)