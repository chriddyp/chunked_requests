chunked-requests
================

A wrapper around Python's httplib for streaming, chunk-encoded HTTP requests

### Usage
```python
from chunked_requests import Stream

stream = Stream('127.0.0.1', 8080)

stream.write('some data')

# take a break, go on a walk

stream.write('some more data') # reconnects if disconnected

response = stream.close()
```

See more in this IPython notebook: [https://github.com/chriddyp/chunked-requests/blob/master/usage.ipynb](https://github.com/chriddyp/chunked-requests/blob/master/usage.ipynb)

### Docs
- `s = Stream(addr, port=80, headers={})`

  Initializes a connection to `addr:port` with `headers`.

- `s.write(data, reconnect=True)`

  Write chunk-encoded data, and reconnect if disconnected.
  
- `response = s.close()`

  Close connection and return a HTTPResponse object

- `int s.maxtries`

  Max number of times to attempt re-connecting before raising an error
