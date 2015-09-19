__author__ = 'cruiz1391'
import socket
import sys
import select
from threading import Thread

host = 'localhost'
server_port = 8000

TUNNEl_CLIENT_ID_SIZE = 36
DATA_SIZE_VALUE = 12
PORT_SIZE_VALUE = 32
BUFFER_SIZE = 2048

HARDCODE_MYCODE = 'fc86c7ef-f579-4115-8137-289b8a257803'
_ACTIVE_CLIENTS_IDS = []
_CLIENT_DEST_SOCKET = {}


def utf8len(s):
    return len(s.encode('utf8'))
#####################################################################################################
def create_tunnel_connection():
    #create a socket object
    tunnel_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tunnel_socket.connect((host, server_port))
    except OSError as msg:
        print(msg)
        tunnel_socket.close()
        sys.exit(0)
    # send tunnel id to server
    tunnel_socket.sendall(HARDCODE_MYCODE)
    tunnel_message = tunnel_socket.recv(TUNNEl_CLIENT_ID_SIZE)
    if(HARDCODE_MYCODE == tunnel_message):
        print("\n Tunnel successfully created! \n")
    else:
        print("\n Error creating tunnel! \n"
              "Message received: ", tunnel_message + "\n")
        tunnel_socket.close()
        sys.exit(0)

    tunnel_thread = Thread(target=tunnel_communication, args=[tunnel_socket])
    tunnel_thread.start()

def tunnel_communication(tunnel_socket):
    #create a socket object
    # local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_readable = [tunnel_socket]
    is_writable = []
    is_error = []
    while True:
        r, w, e = select.select(is_readable, is_writable, is_error, 1.0)
        if r:
            for sock in r:
                if(sock == tunnel_socket):
                    client_ID = tunnel_socket.recv(TUNNEl_CLIENT_ID_SIZE)
                    if(client_ID not in _ACTIVE_CLIENTS_IDS):
                        print ("new server communicating ID: " + client_ID)
                        dest_port = tunnel_socket.recv(PORT_SIZE_VALUE)
                        try:
                            local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            local_socket.connect((host, int(dest_port, 2)))
                        except OSError as msg:
                            print(msg)
                            _CLIENT_DEST_SOCKET[client_ID].close()
                            sys.exit(0)
                        is_readable.append(local_socket)
                        _ACTIVE_CLIENTS_IDS.append(client_ID)
                        _CLIENT_DEST_SOCKET[client_ID] = local_socket

                    data_size = tunnel_socket.recv(DATA_SIZE_VALUE)
                    tunnel_message = tunnel_socket.recv(int(data_size, 2))
                    print('\n------------------------------------\n'
                        'client_ID: '+client_ID+
                        '\nserver message: '+tunnel_message+
                        '\n-----------------------------------\n')
                    dest_socket = _CLIENT_DEST_SOCKET[client_ID]
                    dest_socket.sendall(tunnel_message)
                else:
                    local_message = sock.recv(BUFFER_SIZE)
                    data_send_size = len(local_message)
                    if(data_send_size>0):
                        print('\n------------------------------------\n'
                            'SIZE: '+str(data_send_size)+
                            '\nNEW client message, Sent to server: '+local_message+
                            '\n-----------------------------------\n')
                        for client_id, dest_sock in _CLIENT_DEST_SOCKET.iteritems():
                            if(dest_sock == sock):
                                tunnel_socket.sendall(client_id
                                                      +bytes(bin(data_send_size)[2:].zfill(12))
                                                      +local_message)
        # else:
        #     print "waiting for data to read"

#####################################################################################################
if __name__ == '__main__':
    create_tunnel_connection()
