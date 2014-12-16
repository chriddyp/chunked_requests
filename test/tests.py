import unittest
import os
import errno
import time
from nose.tools import assert_raises

# from chunked_requests import
from chunked_requests.chunked_requests import Stream


class Test(unittest.TestCase):
    def setUp(self):
        pass
        # stream = Stream('127.0.0.1', port=8080)

    def test_successful_write(self):
        ''' Test that data was successfully
        written to the server.
        '''

        _remove_file('request.txt')

        stream = Stream('127.0.0.1',
                        port=8080,
                        url='/successful_write')

        body = 'request-body'*10
        stream.write(body)
        time.sleep(1)
        with open('request.txt', 'r') as f:
            body_from_file = f.read()

        assert(body_from_file == body)

        _remove_file('request.txt')


    def test_reconnect_on_408_timeout(self):
        ''' Test that `reconnect_on` indeed
        reconnects on a `408` timeout response
        from the server after 5 seconds and
        continues to write data. Test that
        all of the data was transmitted, even
        with a broken connection and re-connect.
        '''

        _remove_file('request.txt')

        stream = Stream('127.0.0.1',
                        port=8080,
                        url='/5s_timeout')

        for i in range(8):
            stream.write(str(i),
                         reconnect_on=('', 200, 408))
            time.sleep(1)

        with open('request.txt', 'r') as f:
            body_from_file = f.read()

        body_sent = ''.join([str(i) for i in range(8)])
        assert(body_from_file == body_sent)
        _remove_file('request.txt')


    def test_failure_on_408_timeout(self):
        ''' Test that an error is thrown when
        the server returns a 408 timeout and
        we choose not to reconnect.
        '''

        with assert_raises(Exception) as cm:
            stream = Stream('127.0.0.1',
                            port=8080,
                            url='/5s_timeout')

            for i in range(8):
                stream.write(str(i),
                             reconnect_on=('', 200))
                time.sleep(1)

        ex = cm.exception
        assert(ex.message == "Server responded "
                             "with status code: 408\n"
                             "and message: "
                             "timeout on active data.")

    def test_huge_request_on_latent_server(self):
        _remove_file('request.txt')

        stream = Stream('127.0.0.1',
                        port=9008)
        body = 'x' * (5000 * 1000)
        stream.write(body)

        # Proxy servers delays the response for 10 seconds
        # Writing 5 mill chars takes a bit, so wait a few
        # extra secs before comparing
        time.sleep(13)
        with open('request.txt', 'r') as f:
            body_from_file = f.read()

        assert(body_from_file == body)

        _remove_file('request.txt')


def _remove_file(filename):
    try:
        os.remove(filename)
    except OSError as e:
         # errno.ENOENT = no such file or directory
        if e.errno != errno.ENOENT:
            raise e


if __name__ == '__main__':
    unittest.main()
