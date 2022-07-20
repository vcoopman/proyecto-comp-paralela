import json
import subprocess

def create_exec_string(cond, log, data={}):
    """
    Creates the string runned by the subprocess.
    This string will tell the subprocess to create an envelope function around the condition defined by the user.
    Also 'text' and 'data' variables will be defined inside the subprocess, so the condition can use them.
    Finally it will print to stdout ['True', data] or 'False', depending on the envelope function result.

    Input:
        cond: str # the python condition declared by log detector's user.
        log: dict
        data: dict # machine context data

    Output:
        str
    """

    exec_string = f"""
import json
data={data}
def envelope():
    log={log}
    text="{log['Text']}"
    global data"""
    for line in cond.splitlines():
        exec_string = f"""{exec_string}\n    {line}"""

    exec_string = f"{exec_string}\nprint(json.dumps([True, data])) if envelope() else print(json.dumps([False]))"
    return exec_string


def eval_condition_text(cond, log, data):
    """
    Evaluates a standard condition.

    Inputs:
        cond: str # conditions's text
        log: dict
        data: dict # SM context data

    Returns:
        result: list # list[0] the boolean representing if conditions was True or False.
                     # if condition was True. list[1] will have the updated context data.
    """
    # Prepare exec_string
    exec_string = create_exec_string(cond, log, data)
    print(f"exec_string for eval_condition_text: {exec_string}")

    # Run subprocess/condition 
    result = subprocess.run(['python3', '-c', exec_string], capture_output=True, text=True)
    result.check_returncode() # Raises an Exception if the subprocess ended with one. 

    result = json.loads(result.stdout)

    return result


def create_exec_string_launch_cond(cond, log):
    """
    Creates a string runned by a subprocess.
    The execution of this string will declare a function called: launch(context_data={}).
    The function launch will be usable by the user when defining the launch condition.
    If the user pass context_data to the function, the instance of the SM will start with context_data as context data.

    Around the condition of the user, the subprocess will define and envelope function to wrap up the user python code.

    ------
    input:
        cond: str # user launch condition.
        log: dict
    ------
    returns:
        list # list[0] is the True or False result from the condition.
             # list[1] if True, here will be the context data for the machine.
    """

    # This does looks really ugly, but it needs to be like this, 
    # to keep a correct indentation inside the subprocess.
    exec_string = """
import json
try:
    launch_flag = False
    context = {}
    def launch(data=None):
        global launch_flag
        global context
        launch_flag = True
        context = data

    def envelope():
        text="{}"
        log={}
#here starts user's code
""".format({}, log['Text'], log)

    # add the user code inside envelope function
    for line in cond.splitlines():
        exec_string = f"""{exec_string}\n        {line}"""

    exec_string = f"""
{exec_string}\n
#here ends user's code
    envelope()
    print(json.dumps([launch_flag, context]))
except Exception as ex:
    print(ex)
    raise ex
"""

    return exec_string


def clean_log_text(text: str):
    """ Removes \n symbols in log's text """
    print("cleaning log: ", text)
    print("cleaning log: ", text)
    print("cleaning log: ", text)

    clean_log = text.replace("\n", " ")
    return clean_log

