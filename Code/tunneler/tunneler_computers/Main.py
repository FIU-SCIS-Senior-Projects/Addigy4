__author__ = 'cruiz1391'
import socket
import sys

host = 'localhost'
server_port = 7000
local_port = 8000
BUFFER_ZISE = 1024
CRLF = "\r\n\r\n"


def connect_local_webhost():
    #create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, local_port))
    except OSError as msg:
        print(msg)
        s.close()
        sys.exit(0)
    s.sendall("GET / HTTP/1.0%s" % (CRLF))
    data = (s.recv(1000000))
    print data
    # https://docs.python.org/2/howto/sockets.html#disconnecting
    s.shutdown(1)
    s.close()
    print 'Received', repr(data)



if __name__ == '__main__':
    connect_local_webhost()
