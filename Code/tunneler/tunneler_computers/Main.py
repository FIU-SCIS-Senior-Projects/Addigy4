__author__ = 'cruiz1391'
import socket
import sys

host = 'localhost'
server_port = 8000
local_port = 9000
BUFFER_ZISE = 1024
CRLF = "\r\n\r\n"
HARDCODE_MYCODE = 999999


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
    s.shutdown(1)
    s.close()
    print 'Received', repr(data)
    return data


def create_tunnel_connection():
    #create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, server_port))
    except OSError as msg:
        print(msg)
        s.close()
        sys.exit(0)
    s.sendall(str(HARDCODE_MYCODE))
    while True:
        data = (s.recv(1000000))
        print data
        if("GET / HTTP" in data):
            response = connect_local_webhost()
            print('sending back to server')
            s.sendall(response)



if __name__ == '__main__':
    create_tunnel_connection()
