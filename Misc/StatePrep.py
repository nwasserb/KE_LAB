import pyvisa as visa
from time import sleep


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

    total_mW = port1_mW + port2_mW + port3_mW + port4_mW

    rel_port1_mW = port1_mW / total_mW
    rel_port2_mW = port2_mW / total_mW
    rel_port3_mW = port3_mW / total_mW
    rel_Port4_mW = port4_mW / total_mW

    return [rel_port1_mW, rel_port2_mW, rel_port3_mW, rel_Port4_mW]


#Initialize constants
DETECTOR_RESOURCE_STR = "TCPIP0::10.0.3.17::5000::SOCKET"
EPC_RESOURCE_STR      = "ASRL3::INSTR"
EPC_PREP_RESOURCE_STR      = "ASRL15::INSTR"

#Open PyVISA Sessions
resource_manager = visa.ResourceManager() #PyVISA Resource Manager

detector_session                   = resource_manager.open_resource(DETECTOR_RESOURCE_STR)
detector_session.read_termination  = "\n"
detector_session.write_termination = "\n"

epc_session                   = resource_manager.open_resource(EPC_RESOURCE_STR)
epc_session.read_termination  = "\r\n"
epc_session.write_termination = "\r\n"
epc_session.query_termination = "\r\n"

epc_prep_session                   = resource_manager.open_resource(EPC_PREP_RESOURCE_STR)
epc_prep_session.read_termination  = "\r\n"
epc_prep_session.write_termination = "\r\n"
epc_prep_session.query_termination = "\r\n"

# params = [0, 0, 0, 0]
# epc_query_strings = [f"V{port},{int(inp_voltage)}" for port, inp_voltage in zip(range(1, len(params) + 1), params)]
# for epc_query_string in epc_query_strings:
#     sleep(.05)
#     epc_session.query(epc_query_string)

# Horizontal Max port 1 min port 2 equal 3 and 4
while True:
    params = [0, 0, 0, 0]
    epc_query_strings = [f"V{port},{int(inp_voltage)}" for port, inp_voltage in zip(range(1, len(params) + 1), params)]
    for epc_query_string in epc_query_strings:
        sleep(.05)
        epc_prep_session.query(epc_query_string)
    sleep(.05)


    print("horizontal", read_detector_power_values(detector_session))

    #diagonal Max port 3 min port 4 equal 1 and 2

    v1= int(input("changev1:      "))
    params = [v1, 0, 0, 0]
    epc_query_strings = [f"V{port},{int(inp_voltage)}" for port, inp_voltage in zip(range(1, len(params) + 1), params)]
    for epc_query_string in epc_query_strings:
        sleep(.05)
        epc_prep_session.query(epc_query_string)
    sleep(.05)

    print("diagonal", read_detector_power_values(detector_session))


    #Horizontal Max port 1 min port 2 equal 3 and 4
    params = [0, 0, 0, 0]
    epc_query_strings = [f"V{port},{int(inp_voltage)}" for port, inp_voltage in zip(range(1, len(params) + 1), params)]
    for epc_query_string in epc_query_strings:
        sleep(.05)
        epc_prep_session.query(epc_query_string)
    sleep(.05)


    print("horizontal", read_detector_power_values(detector_session))

