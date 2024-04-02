import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

filename = 'Characterizing_.05delay.csv'
df = pd.read_csv(filename)
num_points = len(df["port1_.05Delay"])
x_values = np.linspace(-5000, 5000, num_points)


plt.figure(figsize=(10, 6))
plt.plot(x_values, df["port1_.05Delay"], label='Port 1 Voltage (mV)')
plt.plot(x_values, df["port2_.05Delay"], label='Port 2 Voltage (mV)')
plt.plot(x_values, df["port3_.05Delay"], label='Port 3 Voltage (mV)')
plt.plot(x_values, df["port4_.05Delay"], label='Port 4 Voltage (mV)')
plt.xlabel('Epoch')
plt.ylabel('Relative power ')
plt.title('Relative Power Vs, Voltages .05 Delay')
plt.legend()
plt.grid(True)
plt.show()