chunked-requests
================

A wrapper around Python's httplib for streaming, chunk-encoded HTTP requests

### Usage
```python
import chunked_requests

stream = chunked_requests('127.0.0.1', 8080)

stream.write('some data')

# take a break, go on a walk

stream.write('some more data') # reconnects if disconnected

response = stream.close()
```

### Docs
- `r = chunked_request(addr, port=80, headers={})`

  Initializes a connection to `addr:port` with `headers`.

- `r.write(data, reconnect=True)`

  Write chunk-encoded data
  
- `response = r.close()`

  Close connection and return a HTTPResponse object

- `int r.maxtries`

  Max number of times to attempt re-connecting before raising an error
