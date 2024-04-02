import pandas as pd
import matplotlib.pyplot as plt

filename_HD = 'EPC_OPTO_SLEEP_HD.csv'
filename_costV = 'EPC_OPTO_SLEEP_costV.csv'

df_HD = pd.read_csv(filename_HD)
df_costV = pd.read_csv(filename_costV)

plt.figure(figsize=(10, 6))
plt.plot(range(len(df_HD.iloc[:, :1])), df_HD["port1_H"], label='Port 1 Power (%)')
plt.plot(range(len(df_HD.iloc[:, :2])), df_HD["port2_H"], label='Port 2 Power (%)')
plt.plot(range(len(df_HD.iloc[:, :3])), df_HD["port3_H"], label='Port 3 Power (%)')
plt.plot(range(len(df_HD.iloc[:, :4])), df_HD["port4_H"], label='Port 4 Power (%)')
plt.xlabel('Epoch')
plt.ylabel('Relative Power (%)')
plt.title('Port Power Vs, Epoch H')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(range(len(df_HD.iloc[:, :1])), df_HD["port1_D"], label='Port 1 Power (%)')
plt.plot(range(len(df_HD.iloc[:, :2])), df_HD["port2_D"], label='Port 2 Power (%)')
plt.plot(range(len(df_HD.iloc[:, :3])), df_HD["port3_D"], label='Port 3 Power (%)')
plt.plot(range(len(df_HD.iloc[:, :4])), df_HD["port4_D"], label='Port 4 Power (%)')
plt.xlabel('Epoch')
plt.ylabel('Relative Power (%)')
plt.title('Port Power Vs, Epoch D')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(range(len(df_costV["V1"])), df_costV["V1"], label='Port 1 Voltage (mV)')
plt.plot(range(len(df_costV["V2"])), df_costV["V2"], label='Port 2 Voltage (mV)')
plt.plot(range(len(df_costV["V3"])), df_costV["V3"], label='Port 3 Voltage (mV)')
plt.plot(range(len(df_costV["V4"])), df_costV["V4"], label='Port 4 Voltage (mV)')
plt.xlabel('Epoch')
plt.ylabel('Port Voltage ')
plt.title('Port Voltage Vs, Epoch')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10,6))
plt.plot(range(len(df_costV["Cost"])),df_costV["Cost"], label='Cost')
plt.xlabel('Epoch')
plt.ylabel('Cost Value')
plt.title('Cost vs Epoch')
plt.legend()
plt.grid(True)
plt.show()