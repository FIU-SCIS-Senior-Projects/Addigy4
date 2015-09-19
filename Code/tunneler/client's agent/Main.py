__author__ = 'cruiz1391'
import uuid
import sys
import socket
import select
from threading import Thread



__CLIENT_LOCAL = 5000
__SERVER_LOCAL = 7000
__HOST = 'localhost'

TUNNEl_CLIENT_ID_SIZE = 36
DATA_SIZE_VALUE = 12
PORT_SIZE_VALUE = 32
BUFFER_SIZE = 2048


_TUNNELCODE = 'fc86c7ef-f579-4115-8137-289b8a257803'
webHost_port = 9000
ssh_port = 22
_LOCAL_ID_DEST_SOCKET = {}

def utf8len(s):
    return len(s.encode('utf8'))
#####################################################################################################
def start_listening_client(__HOST, __CLIENT_LOCAL, __SERVER_LOCAL):
    listen_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_client_socket.bind((__HOST, __CLIENT_LOCAL))
    listen_client_socket.listen(5)
    print ('listening %s ...' % __CLIENT_LOCAL)
    while True:
        client_connection, client_address = listen_client_socket.accept()
        tunnelThread = Thread(target=server_hand_shake, args=[__HOST,
                                                              __SERVER_LOCAL,
                                                              client_connection,
                                                              client_address])
        tunnelThread.start()

#####################################################################################################
def server_hand_shake(__HOST, __REMOTE_LOCAL, client_connection, client_address):
    my_id = uuid.uuid4()
    total_request = client_connection.recv(BUFFER_SIZE)
    size_of_request = len(total_request)
    print ('\n------------------------------------\n'
            'size_of_request: '+str(size_of_request)+
            '\nRequest from CLIENT: '+total_request.decode()+
            '\n------------------------------------\n')

    # TEMP determine endpoint DESIRED PORT: 22 (ssh) or 9000 (webHost)
    start_command = total_request[:3]
    if(start_command == "SSH"):
        dest_port = ssh_port
    else:
        dest_port = webHost_port

    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((__HOST, __REMOTE_LOCAL))
    except OSError as msg:
        print('printing error \n'+msg)
        s.close()
        sys.exit(0)

    # create initial stream to be sent
    initial_server_request = bytes(bin(dest_port)[2:].zfill(32))\
                             +_TUNNELCODE.encode()\
                             +my_id.__str__()\
                             +bytes(bin(size_of_request)[2:].zfill(12))\
                             +total_request

    print("dest_port", dest_port)
    print("dest_tunnel_id", _TUNNELCODE)
    print("client_id", my_id.__str__())
    print("size of request:", size_of_request)
    print("initial_data", total_request)
    print ('------------------------------------\n')
    s.sendall(initial_server_request)
    server_communication(s, client_connection, client_address, my_id)

#####################################################################################################
def server_communication(server_socket, client_connection, client_address, my_id):
    is_readable = [server_socket, client_connection]
    is_writable = []
    is_error = []
    while True:
        r, w, e = select.select(is_readable, is_writable, is_error, 1.0)
        if r:
            for sock in r:
                if(sock == server_socket):
                    data_size = server_socket.recv(DATA_SIZE_VALUE)
                    server_message = server_socket.recv(int(data_size, 2))
                    if(len(server_message) == 0):
                        print('closing connection')
                        client_connection.close()
                        return
                    print('\n------------------------------------\n'
                        'Message from server: '+server_message+
                        '\n-----------------------------------\n')
                    client_connection.sendall(server_message)
                else:
                    client_message = client_connection.recv(BUFFER_SIZE)
                    message_size = len(client_message)
                    if(len(client_message) == 0):
                        print('closing connection')
                        client_connection.close()
                        return

                    data_to_server = _TUNNELCODE.encode() \
                                     + my_id.__str__() \
                                     + bytes(bin(message_size)[2:].zfill(12)) \
                                     + client_message
                    print('\n------------------------------------\n'
                        'NEW MESSAGE SENT TO SERVER: '
                        '\nSIZE _TUNNELCODE: '+_TUNNELCODE+'\n'
                        '\nSIZE my_id.__str__(): '+my_id.__str__()+'\n'
                        '\nmessage_size: '+str(message_size)+'\n'
                        '\ndata to server: '+str(data_to_server)+
                        '\n-----------------------------------\n')
                    server_socket.sendall(data_to_server)
        # else:
        #     print "waiting for data to read"


#####################################################################################################
if __name__ == '__main__':
    print('Starting Client\' Agent')
    start_listening_client(__HOST, __CLIENT_LOCAL, __SERVER_LOCAL)