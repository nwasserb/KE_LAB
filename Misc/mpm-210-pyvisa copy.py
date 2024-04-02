import pyvisa as visa
import time

try:  
    resourceManager = visa.ResourceManager() 
    dev = 'TCPIP0::10.0.0.2::5000::SOCKET'
    session = resourceManager.open_resource(dev)
    print('\n Open Successful!')
    session.read_termination = '\n'
    session.write_termination = '\n'

    result = session.query('READ? 0')
    # Split the string based on the comma (',') separator
    ports = result.split(',')

    # Convert the strings to float numbers
    port1 = float(ports[0].split(':')[-1])
    port2 = float(ports[1])
    port3 = float(ports[2])
    port4 = float(ports[3])

    # Print the values of the variables
    print("===================")
    print("Port 1:", port1)
    print("Port 2:", port2)
    print("Port 3:", port3)
    print("Port 4:", port4)


except Exception as e:
    print('[!] Exception:', str(e))
finally:
    # Close the session when interrupted
    session.close()
