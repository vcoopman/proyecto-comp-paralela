import subprocess
import json
from flask import Flask, request
import utils # local module

app = Flask(__name__)

@app.route("/eval", methods = ['POST'])
def evaluate():
    """
            Eval if conditions true or false.

            ----
            Return:
                trueConditions: integer[] # numeration of true conditions.
                context: dict # The resulting context after evaluating conditions.
    """
    payload = request.json['payload']
    true_conditions = [] # stores numerations of true conditions.
    context = payload['context'] # context to use for this checks. This will be updated after every true condition check.

    print(payload)
    payload['log']['Text'] = utils.clean_log_text(payload['log']['Text'])
    for cond in payload['conditions']:
        if cond['type'] == 'Standard':
            try :
                result = utils.eval_condition_text(cond['text'], payload['log'], context)
                print(result)
                if result[0]:
                    true_conditions.append(cond['numeration'])
                    context = result[1]

            except subprocess.CalledProcessError as e:
                print(e)
                # Ask if this error should be hidden rather than full text
                return { 'error': str(e.stderr), 'condition': cond }

        elif cond['type'] == 'Timed':
            try :
                # Check text
                result1 = utils.eval_condition_text(cond['text'], payload['log'], context)
                print(result1)

                # Check time
                result2 = (payload['logProcessingTime'] - payload['stateTime'] <= cond['timeRange'])

                if result1[0] and result2:
                    true_conditions.append(cond['numeration'])
                    context = result1[1]

            except subprocess.CalledProcessError as e:
                print(e)
                return { 'error': str(e.stderr), 'condition': cond }

        elif cond['type'] == 'Order':
            try:
                all_true_conditions = payload['trueConditions'] + true_conditions
                if len(all_true_conditions) >= len(cond['order']):
                    # Check if order match
                    main_str = ''.join([str(x) for x in all_true_conditions])
                    sub_str = ''.join([str(x) for x in cond['order']])
                    if sub_str in main_str:
                        true_conditions.append(cond['numeration'])

            except Exception as e:
                print(e)
                return { 'error': str(e), 'condition': cond }

    return { 'trueConditions': true_conditions, 'context': context }


@app.route("/eval-launch", methods = ['POST'])
def evaluate_launch():
    """
        Evaluates launch conditions using a subprocess to run user's code.

        ------
        input:
            launchConditions: str[] # User defined conditions.
            log: dict

        ------
        return:
            launch: boolean # if a log detector should be launch or not.
            context: dict # machine context data to start with.

    """
    payload = request.json['payload']
    print(payload)
    payload['log']['Text'] = utils.clean_log_text(payload['log']['Text'])
    cond = payload['launchCondition']
    # create exec string
    exec_string = utils.create_exec_string_launch_cond(cond, payload['log'])

    try:
        # run the exec string
        result = subprocess.run(['python3', '-c', exec_string], capture_output=True, text=True)
        result.check_returncode() # Raises an Exception if the subprocess ended with one. 
        result = json.loads(result.stdout)

        if result[0]:
            return { "condition": cond, "launch": result[0], "context": result[1] }

    except Exception as ex:
        print(ex)
        return { "error": "Error checking launch condition", "launch": False }

    return { "launch": False }

app.run(debug=False, host="0.0.0.0", port=5000)
