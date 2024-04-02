import pandas as pd
import matplotlib.pyplot as plt

# Define the array of numbers
numbers = [.05, .06, .07, .08, .09, .1, .15, .2, .25, .3, .35, .4, .5, .75, 1, 1.5, 2]  # Add more numbers if needed

# Loop over each number
for number in numbers:
    # Construct the filename using string formatting
    filename = f'delay_csv/prep_state_data_{number}.csv'

    # Read data from CSV file
    data = pd.read_csv(filename)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(data['port1_Relative_Power'], label='Port 1')
    plt.plot(data['port2_Relative_Power'], label='Port 2')
    plt.plot(data['port3_Relative_Power'], label='Port 3')
    plt.plot(data['port4_Relative_Power'], label='Port 4')
    plt.xlabel('Time')
    plt.ylabel('Relative Power')
    plt.title(f'Relative Power vs Time (prep_state_data_{number})')
    plt.legend()
    plt.grid(True)
    plt.show()
