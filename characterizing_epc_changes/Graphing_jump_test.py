import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('jump_test_data.csv')



# Create subplots
fig, axs = plt.subplots(4, 1, figsize=(10, 12), sharex=True)
plt.title("STARTED: Port 1: +0.04865% | Port 2: +0.47018% | Port 3: +0.24070% | Port 4: +0.24047%")

# Plot each port on separate subplot
for i, port in enumerate(['port1_Relative_Power', 'port2_Relative_Power', 'port3_Relative_Power', 'port4_Relative_Power']):
    axs[i].plot(df.index * 0.05, df[port])
    axs[i].set_ylabel('Relative Power')
    axs[i].set_title(f'Port {i+1}')

# Add common x-axis label
plt.xlabel('Time (seconds)')

# Adjust layout
plt.tight_layout()


# Show plot
plt.show()