__author__ = 'cruiz1391'
import sys
import socket
import select
from threading import Thread


__tunnel_connection_port = 8000
__client_connection_port = 7000
__HOST = 'localhost'
__client_server = None
__TUNNEL = 0
__CLIENT = 1
_TUNNELS_DIC = {}
_SERVERS = []


def client_tunnel_communication(client_connection):
    # desired tunnel
    request = client_connection.recv(1024)
    if(len(request) == 0):
        print('closing connection')
        client_connection.close()
        return
    print request+"\n"
    desired_tunnel_socket = _TUNNELS_DIC[request]
    client_connection.sendall("connection established")

    while True:
        is_readable = [client_connection, desired_tunnel_socket]
        is_writable = []
        is_error = []
        r, w, e = select.select(is_readable, is_writable, is_error, 1.0)
        if r:
            for sock in r:
                if(sock == client_connection):
                    client_message = client_connection.recv(1024)
                    print('------------------------------------\n'
                        'NEW client_connection message, Sent to tunnel: '
                        '\n\n'
                        +client_message+
                        '-----------------------------------\n')
                    desired_tunnel_socket.sendall(client_message)
                else:
                    tunnel_message = desired_tunnel_socket.recv(1024)
                    if(len(tunnel_message)>0):
                        print('------------------------------------\n'
                            'NEW tunnel message, Sent to client: '
                            '\n\n'
                            +tunnel_message+
                            '-----------------------------------\n')
                        client_connection.sendall(tunnel_message)
        # else:
        #     print "waiting for data to read"

##################################################################################################

def init_clients_sock(__HOST, __client_connection_port):
    listen_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_client_socket.bind((__HOST, __client_connection_port))
    listen_client_socket.listen(5)
    print 'listening %s ...' % __client_connection_port
    while True:
        client_connection, client_address = listen_client_socket.accept()
        client_thread = Thread(target=client_tunnel_communication, args=[client_connection])
        client_thread.start()


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
        request = client_connection.recv(1024)
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

