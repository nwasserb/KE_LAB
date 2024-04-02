import pyvisa as visa


resourceManager = visa.ResourceManager()


dev_EPC = 'ASRL15::INSTR'
session_EPC = resourceManager.open_resource(dev_EPC)
print('\n Open Successful!')
session_EPC.baud_rate = 9600
session_EPC.read_termination = None
session_EPC.write_termination = '\r\n'
session_EPC.query_termination = '\r\n'

session_EPC.query('V1,0')
