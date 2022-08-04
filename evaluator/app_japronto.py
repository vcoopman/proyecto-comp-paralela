from japronto import Application

from eval_func import eval_func # local module

DEBUG = True
PORT = 8000

def evaluate(request):
    payload = request.json['payload']
    r = eval_func(payload)
    return request.Response(json=r)


app = Application()
app.router.add_route("/eval", evaluate)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
