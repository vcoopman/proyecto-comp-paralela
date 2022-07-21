from mpl_toolkits import mplot3d
from optparse import OptionParser
import matplotlib.pyplot as plt
import sys
import csv

usage = '''
    plotter.py -f <input_file>

    Creates a graph reading from <file>.
    '''
parser = OptionParser(usage)
parser.add_option("-f", "--file", dest="input_file", metavar="file",
                  default=None, type=str, help="File to read from.")

(options, args) = parser.parse_args()

if not options.input_file:
    print("No input file!")
    sys.exit(1)

# Read results
clients = []
requests = []
TPRs = [] # time per request
max_TPR = (0, None, None)
min_TPR = (10000, None, None)
avg_TPR = 0
with open(options.input_file, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    line_count = 0
    sum = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')

        current = (int(row['clients']), int(row['log']), float(row['single_log_time']))

        clients.append(current[0])
        requests.append(current[1])
        TPRs.append(current[2])

        if current[2] > max_TPR[0]:
            max_TPR = current
        elif current[2] < min_TPR[0]:
            min_TPR = current

        avg_TPR += current[2]
        line_count += 1

    avg_TPR = float(avg_TPR/line_count)
    print(f'Processed {line_count} lines.')

# print(clients)
# print(requests)
# print(TPRs)
print("MIN: ", min_TPR)
print("MAX: ", max_TPR)
print("AVG: ", avg_TPR)

fig = plt.axes(projection='3d')
fig.plot_trisurf(clients, requests, TPRs, cmap='RdYlGn_r')
fig.set_xlabel('clients')
fig.set_ylabel('requests')
fig.set_zlabel('time per request (ms)')
plt.show()

