__author__ = 'cruiz1391'
import sys
import socket
from threading import Thread


__tunnel_connection_port = 8000
__client_connection_port = 7000
__HOST = 'localhost'
__client_server = None
__TUNNEL = 0
__CLIENT = 1
_TUNNELS_DIC = {}
_SERVERS = []

_REQUEST_CLIENT = "GET / HTTP/1.0%s"

##################################################################################################

def init_clients_sock(__HOST, __http_connection_port):
    listen_http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_http_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_http_socket.bind((__HOST, __http_connection_port))
    listen_http_socket.listen(5)
    print 'listening %s ...' % __http_connection_port
    while True:
        client_connection, client_address = listen_http_socket.accept()
        request = client_connection.recv(1000000)
        if(len(request) == 0):
            print('closing connection')
            listen_http_socket.close()
            return
        print request+"\n"

        client_connection.sendall("connection established")
        next_request = client_connection.recv(1000000)
        print(next_request+"\n")

        socket_to_tunnel = _TUNNELS_DIC[request]
        print('sending request to tunnel')
        socket_to_tunnel.sendall(_REQUEST_CLIENT)
        print('receiving back')
        send_back = socket_to_tunnel.recv(1000000)
        print(send_back)
        client_connection.sendall(send_back)


##################################################################################################

def init_tunnel_sock(__HOST, __tunnel_connection_port):
    buffer = ""
    listen_tunnel_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_tunnel_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_tunnel_socket.bind((__HOST, __tunnel_connection_port))
    listen_tunnel_socket.listen(5)
    print('listening %s ...' % __tunnel_connection_port)
    while True:
        client_connection, client_address = listen_tunnel_socket.accept()
        request = client_connection.recv(1000000)
        _TUNNELS_DIC[request] = client_connection
        print request
        client_connection.sendall("Tunnel created!")
        print _TUNNELS_DIC[request]

##################################################################################################

if __name__ == '__main__':
    print('Server Starting')
    tunnelThread = Thread(target=init_tunnel_sock, args=[__HOST, __tunnel_connection_port])
    tunnelThread.start()
    init_clients_sock(__HOST, __client_connection_port)

