import pyvisa as visa
import time
import math

try:  
    resourceManager = visa.ResourceManager() 
    #print(resourceManager.list_resources())
    dev = 'ASRL3::INSTR'
    session = resourceManager.open_resource(dev)
    print('\n Open Successful!')
    session.read_termination = None
    session.write_termination = '\r\n'
    session.query_termination = '\r\n'

    #Has to have the read because of buffer
    #print(session.query('V?'))
    #  1 read for V?
        
    session.query('V1,4000')
    print(session.read())



except Exception as e:
    print('[!] Exception:', str(e))