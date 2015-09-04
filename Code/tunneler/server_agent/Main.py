__author__ = 'cruiz1391'
import sys
import socket
from threading import Thread


__tunnel_connection_port = 7000
__http_connection_port = 5000
__HOST = 'localhost'
__client_server = None
__TUNNEL = 0
__CLIENT = 1
_TUNNELS = {}
_SERVERS = []

_RESPONSE = 'HTTP/1.0 200 OK\r\nServer: SimpleHTTP/0.6 Python/2.7.9\r\nDate: Thu, 03 Sep 2015 15:23:12 GMT\r\nContent-type: text/html\r\nContent-Length: 178\r\nLast-Modified: Wed, 02 Sep 2015 02:02:24 GMT\r\n\r\n<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <title>Test Localhost</title>\n</head>\n<body>\n<h1>Test localhost server listening:8000</h1>\n</body>\n</html>\n'

##################################################################################################

def init_http_sock(__HOST, __http_connection_port):
    listen_http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_http_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_http_socket.bind((__HOST, __http_connection_port))
    listen_http_socket.listen(5)
    print 'listening %s ...' % __http_connection_port
    while True:
        client_connection, client_address = listen_http_socket.accept()
        request = client_connection.recv(1024)
        print request
        client_connection.sendall(_RESPONSE)
        client_connection.close()

##################################################################################################

def init_tunnel_sock(__HOST, __tunnel_connection_port):
    listen_tunnel_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_tunnel_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_tunnel_socket.bind((__HOST, __tunnel_connection_port))
    listen_tunnel_socket.listen(5)
    print('listening %s ...' % __tunnel_connection_port)
    while True:
        client_connection, client_address = listen_tunnel_socket.accept()
        request = client_connection.recv(1024)
        print request
        client_connection.sendall(_RESPONSE)
        client_connection.close()

##################################################################################################

if __name__ == '__main__':
    print('Server Starting')
    tunnelThread = Thread(target=init_tunnel_sock, args=[__HOST, __tunnel_connection_port])
    tunnelThread.start()
    init_http_sock(__HOST, __http_connection_port)

