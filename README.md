chunked-requests
================

A wrapper around Python's httplib for streaming, chunk-encoded HTTP requests

### Usage
```
import chunked_requests

stream = chunked_requests('127.0.0.1', 8080)

stream.write('some data')

# take a break, go on a walk

stream.write('some more data') # reconnects if disconnected

response = stream.close()
```
