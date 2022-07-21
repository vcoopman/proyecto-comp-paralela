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
with open(options.input_file, mode='r') as csv_file:
  csv_reader = csv.DictReader(csv_file)

  line_count = 0
  for row in csv_reader:
    if line_count == 0:
        print(f'Column names are {", ".join(row)}')

    clients.append(int(row['clients']))
    requests.append(int(row['log']))
    TPRs.append(float(row['single_log_time']))
    line_count += 1

  print(f'Processed {line_count} lines.')

print(clients)
print(requests)
print(TPRs)

fig = plt.figure()
fig = plt.axes(projection='3d')
fig.plot_trisurf(clients, requests, TPRs, cmap=plt.cm.Spectral)
fig.set_xlabel('x')
fig.set_ylabel('requests')
fig.set_zlabel('time per request')
plt.show()
