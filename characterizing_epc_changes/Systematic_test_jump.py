import pyvisa as visa
import time
import math
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import pandas as pd
import threading

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
    while True:
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

# Start the thread for continuous reading
reader_thread = threading.Thread(target=read_data, args=(relPort1mW, relPort2mW, relPort3mW, relPort4mW))
reader_thread.daemon = True
reader_thread.start()
sleep(1.0)



# Loop to perform jumps
jumps = range(50) 
for i in jumps:
    if i == 0:
        sleep(1)
    # Jump from -5000 V to 0
    session_EPC.query('V1,1000')
    # session_EPC.query('V2,1800')
    sleep(.05)  # Delay

    # Jump from 0 to 5000 V
    session_EPC.query('V1,3000')
    # session_EPC.query('V2,0')
    sleep(.05)  # Delay
    if i == 49:
        sleep(1)




session_EPC.close()
sleep(5)

resourceManager = visa.ResourceManager()


dev_EPC = 'ASRL15::INSTR'
session_EPC = resourceManager.open_resource(dev_EPC)
print('\n Open Successful!')
session_EPC.baud_rate = 9600
session_EPC.read_termination = None
session_EPC.write_termination = '\r\n'
session_EPC.query_termination = '\r\n'



# Function to read and process the data
def read_data(relPort1mW, relPort2mW, relPort3mW, relPort4mW):
    while True:
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


# Start the thread for continuous reading
reader_thread = threading.Thread(target=read_data, args=(relPort1mW, relPort2mW, relPort3mW, relPort4mW))
reader_thread.daemon = True
reader_thread.start()
sleep(1.0)

session_EPC.query('V1,-1000')
input()

# Loop to perform jumps
jumps = range(50)  # 10 times as per your requirement
for i in jumps:
    if i == 0:
        sleep(1)
    # Jump from -5000 V to 0
    session_EPC.query('V1,-1000')
    # session_EPC.query('V2,1800')
    sleep(.05)  # Delay

    # Jump from 0 to 5000 V
    session_EPC.query('V1,1000')
    # session_EPC.query('V2,0')
    sleep(.05)  # Delay
    if i == 49:
        sleep(1)




# Plotting the data for Port 1 and Port 3
plt.figure(figsize=(10, 5))

plt.subplot(2, 1, 1)
# plt.plot(np.linspace(0, len(relPort1mW) * .00183599, len(relPort1mW)), relPort1mW, label='Port 1', color='blue')
plt.plot(relPort1mW, label='Port 1', color='blue')
plt.xlabel('Time (s)')
plt.ylabel('Relative Power')
plt.title('Port 1 Relative Power vs Time')
plt.legend()
plt.xticks(np.arange(0, 5, .1))  # Set 10 x ticks

plt.subplot(2, 1, 2)
plt.plot(relPort3mW, label='Port 3', color='orange')
plt.xlabel('Time (s)')
plt.ylabel('Relative Power')
plt.title('Port 3 Relative Power vs Time')
plt.legend()
plt.xticks(np.arange(0, 5, .1))  # Set 10 x ticks

plt.tight_layout()
plt.show()









# Save data to CSV
data = pd.DataFrame({
    "port1_Relative_Power": relPort1mW,
    "port2_Relative_Power": relPort2mW,
    "port3_Relative_Power": relPort3mW,
    "port4_Relative_Power": relPort4mW,
})
data.to_csv('Relative_Power_Data.csv', mode='a', index=False)
