import pandas as pd
import matplotlib.pyplot as plt

# Read data from CSV file
data = pd.read_csv('delay_csv\prep_state_data_0.005.csv')

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(data['port1_Relative_Power'], label='Port 1')
plt.plot(data['port2_Relative_Power'], label='Port 2')
plt.plot(data['port3_Relative_Power'], label='Port 3')
plt.plot(data['port4_Relative_Power'], label='Port 4')
plt.xlabel('Time')
plt.ylabel('Relative Power')
plt.title('Relative Power vs Time')
plt.legend()
plt.grid(True)
plt.show()
