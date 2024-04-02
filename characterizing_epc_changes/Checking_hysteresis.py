import pyvisa as visa
import time
import math
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import pandas as pd

resourceManager = visa.ResourceManager()
dev = 'TCPIP0::10.0.3.17::5000::SOCKET'
session = resourceManager.open_resource(dev)
print('\n Open Successful!')
session.read_termination = '\n'
session.write_termination = '\n'

dev_EPC = 'ASRL15::INSTR'
session_EPC = resourceManager.open_resource(dev_EPC)
print('\n Open Successful!')
session_EPC.baud_rate = 9600
session_EPC.read_termination = None
session_EPC.write_termination = '\r\n'
session_EPC.query_termination = '\r\n'

# Function to read and process the data
def read_data(relPort1mW, relPort2mW, relPort3mW, relPort4mW):
    for i in range(600):
        if i == 0:
            sleep(1)
        # Jump from -5000 V to 0
        session_EPC.query('V3,0')
        sleep(.05)  # Delay

        # Jump from 0 to 5000 V
        session_EPC.query('V3,2700')
        sleep(.05)  # Delay

        session_EPC.query('V3,0')
        sleep(.05)  # Delay
        if i == 599:
            sleep(1)

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

# Read data
read_data(relPort1mW, relPort2mW, relPort3mW, relPort4mW)

# Plot data
plt.figure(figsize=(10, 6))
plt.plot(relPort1mW, label='Port 1')
plt.plot(relPort2mW, label='Port 2')
plt.plot(relPort3mW, label='Port 3')
plt.plot(relPort4mW, label='Port 4')
plt.xlabel('Time')
plt.ylabel('Relative Power')
plt.title('Relative Power vs Time')
plt.legend()
plt.show()
