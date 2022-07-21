#!/bin/python3

# NEXT STEPS:
# 1. Create graph with data. DONE
# 2. Create multiple graphs for differents values. DONE
# 3. Test with real data.
# 4. Integrate scripts. DONE

import sys
import json
import matplotlib.pyplot as plt
import numpy as np
from optparse import OptionParser
from dateutil import parser as dparser


def create_graph(filename, start=None, end=None):
    CPUPerc = []  # CPU usage percent.
    MemPerc = []  # Memory usage percent.
    NetI = []  # Network input.
    NetO = []  # Network output.

    # Parse input.
    # Parse .json created by docker_stats_fetcher.
    with open(filename) as f:
        lines = [line.rstrip() for line in f]
        json_lines = [json.loads(line) for line in lines]

        for obj in json_lines:
            timestamp = dparser.parse(obj['timestamp'])

            # Case start and end.
            if (start and end and start <= timestamp and end >= timestamp) or (start and end is None and start <= timestamp) or (start is None and end is None):
                CPUPerc.append(float(obj['CPUPerc'].replace("%", "")))
                MemPerc.append(float(obj['MemPerc'].replace("%", "")))

                NetI.append(float(obj['NetIO'].split("/")[0][:-3]))
                NetO.append(float(obj['NetIO'].split("/")[1][1:-2]))

    t = np.arange(0.0, len(CPUPerc) * 0.010, 0.010)

    fig, ax = plt.subplots(2, 2)
    fig.canvas.manager.set_window_title(f"Resources graph for {filename}")

    # Adjust graph.
    plt.subplots_adjust(left=0.06, bottom=0.08, right=0.96,
                        top=0.93, wspace=0.15, hspace=0.37)

    # CPU Percent graph.
    ax[0][0].plot(t, CPUPerc)
    ax[0][0].set(xlabel='time (s)', ylabel='CPU Usage (%)',
                 title='CPU Usage over Time.')
    ax[0][0].grid()

    # MemUsage Percent graph.
    ax[0][1].plot(t, MemPerc)
    ax[0][1].set(xlabel='time (s)', ylabel='Memory Usage (%)',
                 title='Memory Usage over Time.')
    ax[0][1].grid()

    # NetIO graph.
    ax[1][0].plot(t, NetI, label="Network Input")
    # ax[1].plot(t, NetO, label="Network Output")
    ax[1][0].set(xlabel='time (s)', ylabel='Network Input (GB)',
                 title='Network Input over Time.')
    ax[1][0].grid()

    ax[1][1].plot(t, NetO, label="Network Output")
    ax[1][1].set(xlabel='time (s)', ylabel='Network Input (MB)',
                 title='Network Output over Time.')
    ax[1][1].grid()

    fig.savefig(f"../graphs/docker-stats-{filename}.png")
    #plt.show()


def main():
    usage = '''
        graph_maker.py -f <file> [options]

        Creates a graph reading from <file> from date <start> to date <end>.
        '''
    parser = OptionParser(usage)
    parser.add_option("-f", "--file", dest="file", metavar="file",
                      default=None, type=str, help="input file.")
    parser.add_option("-s", "--start", dest="start", metavar="start",
                      default=None, type=str, help="time to start from.")
    parser.add_option("-e", "--end", dest="end", metavar="end",
                      default=None, type=str, help="time to end from.")

    (options, args) = parser.parse_args()

    if options.file is None:
        print("ERROR: Missing file")
        sys.exit(1)

    if options.start is not None:
        options.start = dparser.parse(options.start)

    if options.end is not None:
        options.end = dparser.parse(options.end)

    create_graph(options.file, options.start, options.end)


if __name__ == "__main__":
    main()
