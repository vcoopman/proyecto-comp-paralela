import matplotlib.pyplot as plt
import os
import sys
import csv

PATH_TO_FOLDER = "results/multiple_framework/"
files = os.listdir(PATH_TO_FOLDER)

FRAMEWORKS = [ "Flask", "FastAPI", "Falcon", "Japronto" ]
selected_clients = input("Generate graph for how many clients?: (2/4/5/10/20) ")

# Get the data.
Y = []
for file in files:
    print(file)
    framework = file.split("-")[0]

    with open(PATH_TO_FOLDER + file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')

            if row['clients'] == selected_clients:
                Y.append(float(row['single_log_time']))

            line_count += 1

        print(f'Processed {line_count} lines.')

# Plot.
colors = ['green','blue','purple','orange']
plt.bar(FRAMEWORKS, Y, color=colors)
plt.title(f"Time per Request for ({selected_clients}) concurrent clients and 1000 requests in total")
plt.xlabel('Framework', fontsize=14)
plt.ylabel('Time per Request (ms)', fontsize=14)
plt.show()

