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