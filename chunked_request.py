import time
class chunked_request:
    def __init__(self):
        self._maxtries = 5
        self._tries = 0
        self._delay = 1
        self._closed = False
        self.response = None
        self.init()

    def _reset(self):
        self._tries = 0
        self._delay = 1

    def waitforresponse(self):
            self.conn.sock.setblocking(True)
            response = self.conn.sock.recv(500)
            self.conn.sock.setblocking(False)
            return response
        
    def reconnect(self):
        ''' Connect if disconnected.
        Retry with on fibonancii delays
        '''
        if not self.isconnected():
            print 'attempting to re-connect, try #{0}'.format(self._tries)
            try:
                self.init()
            except Exception as e:
                # TODO: Check for "Connection Refused"
                time.sleep(self._delay)
                self._delay += self._delay
                self._tries += 1
                if self._tries < self._maxtries:
                    self.reconnect()
                else:
                    self._reset()
                    raise e
        print 'connected!'
        self._closed = False

    def isconnected(self):
        # First check if we've closed:
        if self._closed:
            print "we closed the connection"
            return False

        # if initialization failed (`self.init()`)
        # then the connection is None
        if self.conn.sock is None:
            return False
    
        # Check if there is any data to be recieved
        # If there is, then the connection has closed
        try:
            response = self.conn.sock.recv(500)
            print response, type(response)
            self.response = response
            print "we found received a response, and we assumed that the response closed the connection"
            return False
        except Exception as e:
            # TODO: How do I just check for "Resource temporarily unavailable"?
            print e
            print "there was nothing in the recv buffer, so i'm assuming we're still open"            
            return True
        
    def init(self):
        self.conn = httplib.HTTPConnection('127.0.0.1', 8080)
        self.conn.putrequest('POST', '/')
        self.conn.putheader('Transfer-Encoding', 'chunked')        
        self.conn.endheaders()
        self.conn.sock.setblocking(False)        
        self._reset()
        
    def write(self, data, reconnect=True):
        if not self.isconnected() and reconnect:
            print 'woops, disconnected. reconnecting...'
            self.reconnect()
        try:
            msg = data
            msglen = format(len(msg), 'x')
            # chunked encoding requests contain the messege length in hex, \r\n, and then the message
            self.conn.send('{msglen}\r\n{msg}\r\n'.format(msglen=msglen, msg=msg))    
        except Exception as e:
            print e
            self.reconnect()
            self.write(data)
            
    def close(self):
        self.conn.send('0\r\n\r\n')
        self.conn.close()
        self._closed = True
        self._reset()
