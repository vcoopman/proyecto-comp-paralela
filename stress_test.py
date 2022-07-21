#!/usr/bin/python3

import sys
import requests
import random
import time
import psutil
import threading
import subprocess
import matplotlib.pyplot as plt
import datetime
from optparse import OptionParser

from payloads import PAYLOADS_EVAL, PAYLOADS_EVAL_LAUNCH  # local module

# SETTINGS.
from settings_scenarios import dummy_settings as settings  # local module
#from settings_scenarios import settings as settings  # local module

# SETTINGS.
EVALUATOR_URL = "http://TESTING_logdetector-evaluator:5000/"  # Target url.
VERBOSE = False

test_number = 1


def kill(proc_pid):
    """
    Util funtion to kill a process.
    """

    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


def send_requests(method, url, payload, request_amount):
    """
    Send request_amount of requests to URL.
    """

    if VERBOSE:
        print(f"URL is: {url}")
        print(f"payload is: {payload}")

    for _ in range(request_amount):
        if method == "GET":
            requests.get(url, json=payload)

        elif method == "POST":
            requests.post(url, json=payload)


def create_test_threads(endpoint, clients, amount):
    """
    Returns clients amount of threads, that execute amount amount of requests.
    """

    url = None
    p_index = None
    method = None
    payload = None

    if endpoint == "eval":
        url = EVALUATOR_URL + "eval"
        p_index = random.randint(0, len(PAYLOADS_EVAL) - 1)
        payload = PAYLOADS_EVAL[p_index]
        payload = {'payload': payload}
        method = "POST"

    elif endpoint == "eval-launch":
        url = EVALUATOR_URL + "eval-launch"
        p_index = random.randint(0, len(PAYLOADS_EVAL_LAUNCH) - 1)
        payload = PAYLOADS_EVAL_LAUNCH[p_index]
        payload = {'payload': payload}
        method = "POST"

    else:
        raise Exception(
            "Unknown endpoint. Endpoints are 'eval' and 'eval-launch'.")

    threads = []
    for _ in range(clients):
        threads.append(threading.Thread(target=send_requests,
                                        args=(method, url, payload, amount)))

    return threads


def run_test_scenario(endpoint, clients, amount, clients_rate=None):
    """
    Execute a test scenario.

    endpoint: Evaluator endpoint to test.
    clients: amount of parallel clients.
    amount: amount of logs/request send per client.
    clients_rate: amount of logdetectors per launcher.

    returns:
    """

    global test_number

    timenow = datetime.datetime.now().strftime("%FT%T")

    print(f"Running Test #{test_number} | {timenow}")

    total_logs = None
    if clients_rate and endpoint == "eval-launch/eval":
        total_logs = amount * (clients + (clients * clients_rate))
        print(
            f"Endpoint: {endpoint}  -  Rate: {clients_rate}  -  Clients: {clients}  -  Logs: {amount}  -  Total Logs: {total_logs}")
        threads_eval_launch = create_test_threads(
            "eval-launch", clients, amount)
        threads_eval = create_test_threads(
            "eval", clients*clients_rate, amount)
        threads = threads_eval + threads_eval_launch
    else:
        total_logs = amount * clients
        print(
            f"Endpoint: {endpoint}  -  Clients: {clients}  -  Logs: {amount}  -  Total Logs: {total_logs}")
        threads = create_test_threads(endpoint, clients, amount)

    start = time.time()

    # Start threads.
    for i, thread in enumerate(threads):
        thread.start()

    # Wait for threads.
    for i, thread in enumerate(threads):
        thread.join()

    end = time.time()
    elapsed = '%.2f' % ((end - start) * 1000)
    single_log_time = '%.3f' % ( float(elapsed)/float(total_logs) )
    print(f"Elapsed: {elapsed} ms")
    print(f"Single Log Time Average: {single_log_time} ms")
    print()

    test_number += 1

    result = {
        'endpoint': endpoint,
        'clients': clients,
        'log': amount,
        'total_logs': total_logs,
        'elapsed': elapsed,
        'test#': test_number,
        'single_log_time': single_log_time
    }
    if clients_rate:
        result['rate'] = clients_rate
    return result


def scenario_0():
    """
    Test eval endpoint.
    """

    log_amount = settings['0']['log_amount']
    client_count = settings['0']['client_count']

    results = []
    for clients in client_count:
        for amount in log_amount:
            results.append(run_test_scenario("eval", clients, amount))

    return results


def scenario_1():
    """
    Test eval-launch endpoint.
    """

    log_amount = settings['1']['log_amount']
    client_count = settings['1']['client_count']

    results = []
    for clients in client_count:
        for amount in log_amount:
            results.append(run_test_scenario("eval-launch", clients, amount))

    return results


def scenario_2():
    """
    Test eval-launch and eval endpoints.
    """

    log_amount = settings['2']['log_amount']
    client_count = settings['2']['client_count']
    launcher_logdetector_rates = settings['2']['rate']

    results = []
    for rate in launcher_logdetector_rates:
        for clients in client_count:
            for amount in log_amount:
                results.append(run_test_scenario(
                    "eval-launch/eval", clients, amount, rate))

    return results


def plot_scenario(x, y, title):
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title(title)
    fig.set_size_inches(20, 10)
    plt.subplots_adjust(left=0.06, bottom=0.20, right=0.96,
                        top=0.95, wspace=0.15, hspace=0.37)
    plt.xticks(rotation=45)
    ax.plot(x, y)

    if title == "Scenario 2":
        ax.set(xlabel='sub-scenario (endpoint|clients|rate|logs)', ylabel='elapsed (ms)',
               title=title)
    else:
        ax.set(xlabel='sub-scenario (endpoint|clients|logs)', ylabel='elapsed (ms)',
               title=title)

    ax.grid()
    plt.show(block=False)

    timenow = datetime.datetime.now().strftime("%FT%T")
    plt.savefig(f"graphs/{title}-{timenow}", bbox_inches='tight')


def main():
    # Start docker_stats_fetcher.
    # cmd = f"cd docker_stats_fetcher; ./docker_stats_fetcher.sh {container}"
    # p1 = subprocess.Popen(cmd, shell=True)

    while True:
        print("Which scenario do you want to run?")
        print("[0] eval")
        print("[1] eval-launch")
        print("[2] eval-launch / eval")
        print("[3] all")
        print()
        print("[4] exit")
        scenario = int(input())

        if scenario == 0:
            results = scenario_0()

            x = []
            y = []
            elapsed = 0.0
            total_logs = 0
            for r in results:
                x.append(f"{r['endpoint']}|{r['clients']}|{r['log']}")
                y.append(float(r['elapsed']))
                elapsed += float(r['elapsed'])
                total_logs += r['total_logs']

            print(f"Scenario 0 - Total Logs: {total_logs} - Elapsed: {'%.2f' % elapsed} ms - Single Log Time Average: {'%.2f' % ( elapsed/float(total_logs) )} ms")
            print()

            plot_scenario(x, y, "Scenario 0")

        elif scenario == 1:
            results = scenario_1()

            x = []
            y = []
            elapsed = 0.0
            total_logs = 0
            for r in results:
                x.append(f"{r['endpoint']}|{r['clients']}|{r['log']}")
                y.append(float(r['elapsed']))
                elapsed += float(r['elapsed'])
                total_logs += r['total_logs']

            print(f"Scenario 1 - Total Logs: {total_logs} - Elapsed: {'%.2f' % elapsed} ms - Single Log Time Average: {'%.2f' % ( elapsed/float(total_logs) )} ms")
            print()

            plot_scenario(x, y, "Scenario 1")

        elif scenario == 2:
            results = scenario_2()

            x = []
            y = []
            elapsed = 0.0
            total_logs = 0
            for r in results:
                x.append(
                    f"{r['endpoint']}|{r['clients']}|{r['rate']}|{r['log']}")
                y.append(float(r['elapsed']))
                elapsed += float(r['elapsed'])
                total_logs += r['total_logs']

            print(f"Scenario 2 - Total Logs: {total_logs} - Elapsed: {'%.2f' % elapsed} ms - Single Log Time Average: {'%.2f' % ( elapsed/float(total_logs) )} ms")
            print()

            plot_scenario(x, y, "Scenario 2")

        elif scenario == 3:
            results = scenario_0()
            x = []
            y = []
            elapsed = 0.0
            total_logs = 0
            for r in results:
                x.append(f"{r['endpoint']}|{r['clients']}|{r['log']}")
                y.append(float(r['elapsed']))
                elapsed += float(r['elapsed'])
                total_logs += r['total_logs']
            print(f"Scenario 0 - Total Logs: {total_logs} - Elapsed: {'%.2f' % elapsed} ms - Single Log Time Average: {'%.2f' % ( elapsed/float(total_logs) )} ms")
            print()
            plot_scenario(x, y, "Scenario 0")

            results = scenario_1()
            x = []
            y = []
            elapsed = 0.0
            total_logs = 0
            for r in results:
                x.append(f"{r['endpoint']}|{r['clients']}|{r['log']}")
                y.append(float(r['elapsed']))
                elapsed += float(r['elapsed'])
                total_logs += r['total_logs']
            print(f"Scenario 1 - Total Logs: {total_logs} - Elapsed: {'%.2f' % elapsed} ms - Single Log Time Average: {'%.2f' % ( elapsed/float(total_logs) )} ms")
            print()
            plot_scenario(x, y, "Scenario 1")

            results = scenario_2()
            x = []
            y = []
            elapsed = 0.0
            total_logs = 0
            for r in results:
                x.append(
                    f"{r['endpoint']}|{r['clients']}|{r['rate']}|{r['log']}")
                y.append(float(r['elapsed']))
                elapsed += float(r['elapsed'])
                total_logs += r['total_logs']
            print(f"Scenario 2 - Total Logs: {total_logs} - Elapsed: {'%.2f' % elapsed} ms - Single Log Time Average: {'%.2f' % ( elapsed/float(total_logs) )} ms")
            print()
            plot_scenario(x, y, "Scenario 2")

        elif scenario == 4:
            print("Exit.")
            break

        else:
            print("Scenario not found.")

    # Clean.
    #if p1 is not None:
    #    try:
    #        p1.wait(timeout=0.1)
    #    except subprocess.TimeoutExpired:
    #        kill(p1.pid)


if __name__ == "__main__":
    usage = '''
        stress_test.py -c <container_id>

        Creates a graph reading from <file> from date <start> to date <end>.
        '''
    parser = OptionParser(usage)
    parser.add_option("-c", "--container", dest="container", metavar="container",
                      default=None, type=str, help="docker container where to test.")

    (options, args) = parser.parse_args()

    main()
