import falcon

from eval_func import eval_func # local module

DEBUG = True
PORT = 5000

class EvalResource:

    def on_post(self, req, resp):
        payload = req.media['payload']
        r = eval_func(payload)
        req.media['payload'] = r

app = falcon.App()
app.add_route('/eval', EvalResource())

if __name__ == '__main__':
    with make_server('', PORT, app) as httpd:
        print(f'Serving on port { PORT }')

        httpd.serve_forever()
