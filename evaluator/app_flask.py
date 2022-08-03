from flask import Flask, request

from eval_func import eval_func # local module

DEBUG = True
PORT = 5000

app = Flask(__name__)

@app.route("/eval", methods = ['POST'])
def evaluate():
    payload = request.json['payload']
    r = eval_func(payload)
    return r

if __name__ == '__main__':
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
