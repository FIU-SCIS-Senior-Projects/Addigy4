__author__ = 'cruiz1391'
import sys
import socket
import select
from threading import Thread


__tunnel_connection_port = 8000
__client_connection_port = 7000
__HOST = 'localhost'
_TUNNELS_DIC = {}
_CLIENTS_DIC = {}
_TUNNELS_ON_SELECT = []

TUNNEl_CLIENT_ID_SIZE = 36
DATA_SIZE_VALUE = 12
PORT_SIZE_VALUE = 32



def client_tunnel_communication(client_connection, client_address):
    is_readable = [client_connection]
    is_writable = []
    is_error = []
    while True:
        r, w, e = select.select(is_readable, is_writable, is_error, 1.0)
        if r:
            tunnel_dest_id = client_connection.recv(TUNNEl_CLIENT_ID_SIZE)
            client_id = client_connection.recv(TUNNEl_CLIENT_ID_SIZE)
            data_size = client_connection.recv(DATA_SIZE_VALUE)
            client_message = client_connection.recv(int(data_size, 2))

            print('\n------------------------------------\n'
                'NEW MESSAGE FROM CLIENT: '
                '\ntunnel_dest_id: '+tunnel_dest_id+
                '\nclient_id: '+client_id+
                '\ndata_size: '+str(int(data_size, 2))+
                '\nclient_message: '+client_message+
                '\n-----------------------------------\n')

            _TUNNELS_DIC[tunnel_dest_id].sendall(client_id+bytes(data_size)+client_message)
        # else:
        #     print "waiting for data to read"
##################################################################################################

def tunnels_incomming_messages_handler():
    print("listening to tunnels on select......")
    while True:
        is_writable = []
        is_error = []
        r, w, e = select.select(_TUNNELS_ON_SELECT, is_writable, is_error, 1.0)
        if r:
            for sock in r:
                client_id = sock.recv(TUNNEl_CLIENT_ID_SIZE)
                data_size = sock.recv(DATA_SIZE_VALUE)
                tunnel_message = sock.recv(int(data_size,2))
                print('\n------------------------------------\n'
                    'destination client_id: '+client_id+
                    '\nNEW tunnel message Sent to client: '+tunnel_message+
                    '\n-----------------------------------\n')
                if(len(tunnel_message) == 0):
                    print('closing tunnel connection: ')
                    sock.close()
                    _TUNNELS_ON_SELECT.remove(sock)
                    return
                _CLIENTS_DIC[client_id].sendall(bytes(data_size) + tunnel_message)
        # else:vevo 2015
        #     print "waiting for data to read"


##################################################################################################

def client_tunnel_setup(client_connection, client_address):
    # receive destination port from tunnel
    dest_port = client_connection.recv(PORT_SIZE_VALUE)
    print("dest_port", int(dest_port, 2))
    #receive dest_tunnel_ID
    dest_tunnel_id = client_connection.recv(TUNNEl_CLIENT_ID_SIZE)
    print("dest_tunnel_id", dest_tunnel_id)
    #receive client ID
    client_id = client_connection.recv(TUNNEl_CLIENT_ID_SIZE)
    print("client_id", client_id)
    # size of data
    data_size_to_read = client_connection.recv(DATA_SIZE_VALUE)
    # receive initial data to be send to tunnel end point
    initial_data = client_connection.recv(int(data_size_to_read, 2))
    print("initial_data", initial_data)

    _CLIENTS_DIC[client_id] = client_connection
    if(dest_tunnel_id not in _TUNNELS_ON_SELECT):
        _TUNNELS_ON_SELECT.append(_TUNNELS_DIC[dest_tunnel_id])

    client_tunnel_handShake = client_id + bytes(dest_port) + bytes(data_size_to_read) + initial_data
    desired_tunnel_socket = _TUNNELS_DIC[dest_tunnel_id]
    desired_tunnel_socket.sendall(client_tunnel_handShake)


##################################################################################################

def init_clients_sock(__HOST, __client_connection_port):
    listen_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_client_socket.bind((__HOST, __client_connection_port))
    listen_client_socket.listen(5)
    print 'listening %s ...' % __client_connection_port
    while True:
        client_connection, client_address = listen_client_socket.accept()
        client_tunnel_setup(client_connection, client_address)
        client_thread = Thread(target=client_tunnel_communication, args=[client_connection, client_address])
        client_thread.start()


##################################################################################################

def init_tunnel_sock(__HOST, __tunnel_connection_port):
    thread_running = False
    listen_tunnel_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_tunnel_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_tunnel_socket.bind((__HOST, __tunnel_connection_port))
    listen_tunnel_socket.listen(5)
    print('listening %s ...' % __tunnel_connection_port)
    while True:
        tunnel_connection, tunnel_address = listen_tunnel_socket.accept()
        # receiving tunnel uuid
        tunnel_id = tunnel_connection.recv(TUNNEl_CLIENT_ID_SIZE)
        _TUNNELS_DIC[tunnel_id] = tunnel_connection
        print ('\n------------------------------------\n'
               "New tunnel connection established!"
               "\ntunnelID: "+ tunnel_id + ""
               '\n------------------------------------\n')
        tunnel_connection.sendall(tunnel_id)


##################################################################################################

if __name__ == '__main__':
    print('Server Starting')
    # listen to tunnels incoming DATA
    tunnels_on_select = Thread(target=tunnels_incomming_messages_handler)
    tunnels_on_select.start()
    # starting socket to listen for incoming connections from tunnels
    tunnelThread = Thread(target=init_tunnel_sock, args=[__HOST, __tunnel_connection_port])
    tunnelThread.start()
    # listen for incoming client connections
    init_clients_sock(__HOST, __client_connection_port)

