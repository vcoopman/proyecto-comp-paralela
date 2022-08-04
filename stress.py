#!/usr/bin/python3

import csv
import requests
import random
import time
import psutil
import threading
import subprocess
import datetime
from optparse import OptionParser

from payloads import PAYLOADS_EVAL  # local module
from settings_scenarios import settings_2 as settings  # local module

EVALUATOR_FLASK = ("http://localhost:5000", "flask")
EVALUATOR_FALCON = ("http://localhost:6000", "falcon")
EVALUATOR_FASTAPI = ("http://localhost:7000", "fastapi")
EVALUATOR_JAPRONTO = ("http://localhost:8000", "japronto")

EVALUATOR_URLS = [ EVALUATOR_FLASK, EVALUATOR_FALCON, EVALUATOR_FASTAPI, EVALUATOR_JAPRONTO ]

VERBOSE = True

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

    for _ in range(request_amount):
        res = None
        if method == "GET":
            res = requests.get(url, json=payload)
        elif method == "POST":
            res = requests.post(url, json=payload)
        # print(res.json())


def create_test_threads(url, clients, amount):
    """
    Returns clients amount of threads, that execute amount of requests.
    """
    method = "POST"

    # Fix to send fixed amount of logs.
    # Amount is divided amount the clients.
    amount = int(amount / clients)

    threads = []
    for cli in range(clients):
        if VERBOSE: print(f"client {cli} will send {amount} requests to {url}")

        p_index = random.randint(0, len(PAYLOADS_EVAL) - 1)
        payload = PAYLOADS_EVAL[p_index]
        payload = {'payload': payload}

        threads.append(threading.Thread(target=send_requests,
                                        args=(method, url, payload, amount)))

    return threads


def run_test_scenario(url, clients, logs):
    """
    Execute a test of a scenario.

    url: Evaluator endpoint to test.
    clients: amount of parallel clients.
    logs: amount of logs to send (in total).
    """

    global test_number

    timenow = datetime.datetime.now().strftime("%FT%T")

    print(f"Running Test #{test_number} | {timenow}")

    print(f"url: {url}")
    print(f"clients: {clients}")
    print(f"logs: {logs}")
    threads = create_test_threads(url, clients, logs)

    start = time.time()

    # Start threads.
    for i, thread in enumerate(threads):
        thread.start()

    # Wait for threads.
    for i, thread in enumerate(threads):
        thread.join()

    end = time.time()
    elapsed = '%.2f' % ((end - start) * 1000)
    single_log_time = '%.3f' % ( float(elapsed)/float(logs) )
    print(f"Elapsed: {elapsed} ms")
    print(f"Single Log Time Average: {single_log_time} ms")
    print()

    test_number += 1

    result = {
        'clients': clients,
        'logs': logs,
        'elapsed': elapsed,
        'test#': test_number,
        'single_log_time': single_log_time
    }

    return result


def scenario_0(url):
    """
    Test eval endpoint against the url url.
    """

    if VERBOSE:
        print(" == TEST SETTINGS ==")
        print(f"LOGS: {settings['0']['log_amount']}")
        print(f"CLIENTS: {settings['0']['client_count']}")
        print()

    log_amount = settings['0']['log_amount']
    client_count = settings['0']['client_count']

    results = []
    for clients in client_count:
        for amount in log_amount:
            results.append(run_test_scenario(f"{url}/eval", clients, amount))

    return results


# def scenario_1():
    # """
    # Test eval-launch endpoint.
    # """

    # log_amount = settings['1']['log_amount']
    # client_count = settings['1']['client_count']

    # results = []
    # for clients in client_count:
        # for amount in log_amount:
            # results.append(run_test_scenario("eval-launch", clients, amount))

    # return results


# def scenario_2():
    # """
    # Test eval-launch and eval endpoints.
    # """

    # log_amount = settings['2']['log_amount']
    # client_count = settings['2']['client_count']
    # launcher_logdetector_rates = settings['2']['rate']

    # results = []
    # for rate in launcher_logdetector_rates:
        # for clients in client_count:
            # for amount in log_amount:
                # results.append(run_test_scenario(
                    # "eval-launch/eval", clients, amount, rate))

    # return results


# def plot_scenario(x, y, title):
    # fig, ax = plt.subplots()
    # fig.canvas.manager.set_window_title(title)
    # fig.set_size_inches(20, 10)
    # plt.subplots_adjust(left=0.06, bottom=0.20, right=0.96,
                        # top=0.95, wspace=0.15, hspace=0.37)
    # plt.xticks(rotation=45)
    # ax.plot(x, y)

    # if title == "Scenario 2":
        # ax.set(xlabel='sub-scenario (endpoint|clients|rate|logs)', ylabel='elapsed (ms)',
               # title=title)
    # else:
        # ax.set(xlabel='sub-scenario (endpoint|clients|logs)', ylabel='elapsed (ms)',
               # title=title)

    # ax.grid()
    # plt.show(block=False)

    # timenow = datetime.datetime.now().strftime("%FT%T")
    # plt.savefig(f"graphs/{title}-{timenow}", bbox_inches='tight')


def main():
    # Start docker_stats_fetcher.
    # cmd = f"cd docker_stats_fetcher; ./docker_stats_fetcher.sh {container}"
    # p1 = subprocess.Popen(cmd, shell=True)

    print(f"EVALUATOR URLS: {EVALUATOR_URLS}\n")

    while True:
        print("Which scenario do you want to run?")
        print("[0] eval multiple frameworks")
        print("[1] eval variable gunicorn workers")
        # print("[2] eval-launch / eval")
        # print("[3] all")
        print()
        print("[4] exit")
        scenario = int(input())

        if scenario == 0:
            for url in EVALUATOR_URLS:
                results = scenario_0(url[0])

                # Write results to csv.
                app_framework = url[1]
                timenow = datetime.datetime.now().strftime("%FT%H-%M-%S")
                results_file = f"results/{app_framework}-eval-{timenow}.csv"
                with open(results_file, mode='w') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=results[0].keys())
                    writer.writeheader()

                    for result in results:
                        writer.writerow(result)

                elapsed_scenario = 0.0
                total_logs = 0
                for r in results:
                    elapsed_scenario += float(r['elapsed'])
                    total_logs += r['logs']

                print(f"Scenario 0 - Total Logs: {total_logs} - Elapsed: {'%.2f' % elapsed_scenario} ms - Time per Request (AVG): {'%.2f' % ( elapsed_scenario/float(total_logs) )} ms")
                print()

        elif scenario == 1:
            framework_index = int(input(f"Selected a web framework: { [ (i, fw[1]) for i, fw in enumerate(EVALUATOR_URLS)] }: "))
            url, framework = EVALUATOR_URLS[framework_index][0], EVALUATOR_URLS[framework_index][1]
            container_name = f"evaluator_logdetector-evaluator-{framework}_1"

            def reduce_worker_count(container_name):
                subprocess.call(['docker', 'exec', '-it', container_name, 'kill', '-TTOU', '1'])

            def increase_worker_count(container_name):
                subprocess.call(['docker', 'exec', '-it', container_name, 'kill', '-TTIN', '1'])

            def clean_workers(container_name):
                for _ in range(50):
                    reduce_worker_count(container_name)

            for wc in settings['1']['worker_count']:
                clean_workers(container_name)

                print(f"Setting {wc} workers...")
                for _ in range(wc):
                    increase_worker_count(container_name)

                time.sleep(1) # wait for the workers to boot up.

                results = scenario_0(url)

                # Add workers to results.
                for r in results:
                    r['workers'] = wc

                # Write results to csv.
                timenow = datetime.datetime.now().strftime("%FT%H-%M-%S")
                results_file = f"results/{framework}-eval-{wc}-{timenow}.csv"
                with open(results_file, mode='w') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=results[0].keys())
                    writer.writeheader()

                    for result in results:
                        writer.writerow(result)

                elapsed_scenario = 0.0
                total_logs = 0
                for r in results:
                    elapsed_scenario += float(r['elapsed'])
                    total_logs += r['logs']

                print(f"Scenario 1 - Total Logs: {total_logs} - Elapsed: {'%.2f' % elapsed_scenario} ms - Time per Request (AVG): {'%.2f' % ( elapsed_scenario/float(total_logs) )} ms")
                print()


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
