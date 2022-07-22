
Avance 1: proyecto semestral 
Introduccion a la Computacion Paralela 
=======================================

== 2022/05/19 ==

1. Preparar test de rendimiento.
DONE

2. Testar en distintos escenarios.
ref: https://www.cardinalpeak.com/blog/faster-python-with-cython-and-pypy-part-1 

3. investigar herramientas/opciones.

== 2022/05/20 ==

1. Prepare stress test.
  concurrent users [x]
  users types (launcher/logdetector) [x]
  real payload [ ] (ingesting)

  Maquina: SelfTestMachine
  Start date: 2019-10-13 14:12:00.000
  End date: 2019-10-13 14:45:00.000

3. investigar herramientas/opciones.
https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface
docker stats fetcher >> parser into graph. 
https://docs.locust.io/en/stable/quickstart.html # tool to do stress test.
https://superuser.openstack.org/articles/run-load-balanced-service-docker-containers-openstack/  # how to create reverse proxy.

# NEXT STEPS:
# -1 finish graph_maker.
# -2 get real payloads. 
# -3 run tests.
# -4 investigate options to optimize.

== 2022/05/22 ==

# -1 finish graph_maker.
DONE
# -2 get real payloads. 
DONE
# -3 run tests.


Running Test #270 | 2022-05-23T03:07:43
Endpoint: eval-launch/eval  -  Rate: 5  -  Clients: 5  -  Logs: 500  -  Total Logs: 15000
Elapsed: 88756.55 ms
Single Log Time Average: 5.917 ms

Scenario 2 - Total Logs: 453750 - Elapsed: 2835718.81 ms - Single Log Time Average: 6.25 ms

ERRORS LAST TEST:

Exception in thread Thread-2256:
Traceback (most recent call last):
  File "/home/vcoopman/.local/share/virtualenvs/proyecto-Xx0NZDcT/lib/python3.8/site-packages/urllib3/connectionpool.py", line 703, in urlopen
    httplib_response = self._make_request(
  File "/home/vcoopman/.local/share/virtualenvs/proyecto-Xx0NZDcT/lib/python3.8/site-packages/urllib3/connectionpool.py", line 398, in _make_request
    conn.request(method, url, **httplib_request_kw)
  File "/home/vcoopman/.local/share/virtualenvs/proyecto-Xx0NZDcT/lib/python3.8/site-packages/urllib3/connection.py", line 239, in request
    super(HTTPConnection, self).request(method, url, body=body, headers=headers)
  File "/usr/lib/python3.8/http/client.py", line 1256, in request
    self._send_request(method, url, body, headers, encode_chunked)
  File "/usr/lib/python3.8/http/client.py", line 1302, in _send_request
    self.endheaders(body, encode_chunked=encode_chunked)
  File "/usr/lib/python3.8/http/client.py", line 1251, in endheaders
    self._send_output(message_body, encode_chunked=encode_chunked)
  File "/usr/lib/python3.8/http/client.py", line 1050, in _send_output
    self.send(chunk)
  File "/usr/lib/python3.8/http/client.py", line 972, in send
    self.sock.sendall(data)
ConnectionResetError: [Errno 104] Connection reset by peer

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/vcoopman/.local/share/virtualenvs/proyecto-Xx0NZDcT/lib/python3.8/site-packages/requests/adapters.py", line 440, in send
    resp = conn.urlopen(
  File "/home/vcoopman/.local/share/virtualenvs/proyecto-Xx0NZDcT/lib/python3.8/site-packages/urllib3/connectionpool.py", line 785, in urlopen
    retries = retries.increment(
  File "/home/vcoopman/.local/share/virtualenvs/proyecto-Xx0NZDcT/lib/python3.8/site-packages/urllib3/util/retry.py", line 550, in increment
    raise six.reraise(type(error), error, _stacktrace)
  File "/home/vcoopman/.local/share/virtualenvs/proyecto-Xx0NZDcT/lib/python3.8/site-packages/urllib3/packages/six.py", line 769, in reraise
    raise value.with_traceback(tb)
  File "/home/vcoopman/.local/share/virtualenvs/proyecto-Xx0NZDcT/lib/python3.8/site-packages/urllib3/connectionpool.py", line 703, in urlopen
    httplib_response = self._make_request(
  File "/home/vcoopman/.local/share/virtualenvs/proyecto-Xx0NZDcT/lib/python3.8/site-packages/urllib3/connectionpool.py", line 398, in _make_request
    conn.request(method, url, **httplib_request_kw)
  File "/home/vcoopman/.local/share/virtualenvs/proyecto-Xx0NZDcT/lib/python3.8/site-packages/urllib3/connection.py", line 239, in request
    super(HTTPConnection, self).request(method, url, body=body, headers=headers)
  File "/usr/lib/python3.8/http/client.py", line 1256, in request
    self._send_request(method, url, body, headers, encode_chunked)
  File "/usr/lib/python3.8/http/client.py", line 1302, in _send_request
    self.endheaders(body, encode_chunked=encode_chunked)
  File "/usr/lib/python3.8/http/client.py", line 1251, in endheaders
    self._send_output(message_body, encode_chunked=encode_chunked)
  File "/usr/lib/python3.8/http/client.py", line 1050, in _send_output
    self.send(chunk)
  File "/usr/lib/python3.8/http/client.py", line 972, in send
    self.sock.sendall(data)
urllib3.exceptions.ProtocolError: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3.8/threading.py", line 932, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.8/threading.py", line 870, in run
    self._target(*self._args, **self._kwargs)
  File "stress_test.py", line 47, in send_requests
    requests.post(url, json=payload)
  File "/home/vcoopman/.local/share/virtualenvs/proyecto-Xx0NZDcT/lib/python3.8/site-packages/requests/api.py", line 117, in post
    return request('post', url, data=data, json=json, **kwargs)
  File "/home/vcoopman/.local/share/virtualenvs/proyecto-Xx0NZDcT/lib/python3.8/site-packages/requests/api.py", line 61, in request
    return session.request(method=method, url=url, **kwargs)
  File "/home/vcoopman/.local/share/virtualenvs/proyecto-Xx0NZDcT/lib/python3.8/site-packages/requests/sessions.py", line 529, in request
    resp = self.send(prep, **send_kwargs)
  File "/home/vcoopman/.local/share/virtualenvs/proyecto-Xx0NZDcT/lib/python3.8/site-packages/requests/sessions.py", line 645, in send
    r = adapter.send(request, **kwargs)
  File "/home/vcoopman/.local/share/virtualenvs/proyecto-Xx0NZDcT/lib/python3.8/site-packages/requests/adapters.py", line 501, in send
    raise ConnectionError(err, request=request)
requests.exceptions.ConnectionError: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
