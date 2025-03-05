import serial.tools.list_ports
import serial
import time
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import datetime

# List all available ports
ports = serial.tools.list_ports.comports()
portsList = []

for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

val = 2

# Determine the selected port
for x in range(0, len(portsList)):
    if portsList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portVar)

# Setup the serial connection
serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()

# Initialize data containers for plotting
times = deque(maxlen=100)  # Adjust the maxlen to 100
values = deque(maxlen=100)  # Adjust the maxlen to 100
data_points_collected = 0  # Counter for data points collected

# Open a CSV file to store the data (anik_data.csv)
with open('anik_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # Delay for 3 seconds before starting to record
    time.sleep(3)

    # Start time for recording
    start_time = time.time()

    # Function to collect data from Arduino and write to CSV
    def collect_data():
        global data_points_collected
        while data_points_collected < 100:  # Continue until the first 100 data points are collected
            if serialInst.in_waiting:
                packet = serialInst.readline().decode('utf').rstrip('\n')
                try:
                    data_point = int(packet)
                    current_time = time.time() - start_time
                    times.append(current_time)
                    values.append(data_point)
                    data_points_collected += 1
                    print(f'{data_point}')
                    writer.writerow([current_time, data_point])  # Write data to CSV
                    file.flush()  # Ensure the data is written immediately to the file
                except ValueError:
                    pass

    # Set up the plot
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)

    def init():
        ax.set_ylim(150, 950)  # Adjust y-axis limits based on your data range
        ax.set_xlim(0, 10)  # Adjust as needed
        return line,

    def update(frame):
        line.set_data(times, values)
        ax.relim()
        ax.autoscale_view()
        ax.set_xlim(max(0, max(times) - 10), max(times))  # Update x-axis limits based on data
        return line,

    ani = animation.FuncAnimation(fig, update, init_func=init, blit=True)
    plt.show()

# Close the serial connection
serialInst.close()
