__author__ = 'cruiz1391'
import sys
import socket
import select
from threading import Thread

__CLIENT_LOCAL = 5000
__SSH_CLIENT_LOCAL = 5050
__SERVER_LOCAL = 7000
__HOST = 'localhost'
_TUNNELCODE = 999999

webHost_port = 9000
ssh_port = 22
#####################################################################################################
def start_listening_client(__HOST, __CLIENT_LOCAL, __SERVER_LOCAL):
    listen_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_client_socket.bind((__HOST, __CLIENT_LOCAL))
    listen_client_socket.listen(5)
    print 'listening %s ...' % __CLIENT_LOCAL
    while True:
        client_connection, client_address = listen_client_socket.accept()
        tunnelThread = Thread(target=server_hand_shake, args=[__HOST,
                                                              __SERVER_LOCAL,
                                                              client_connection,
                                                              client_address])
        tunnelThread.start()

#####################################################################################################
def server_hand_shake(__HOST, __REMOTE_LOCAL, client_connection, client_address):
    total_request = client_connection.recv(1024)
    print '------------------------------------\n' \
          'Request from CLIENT:' \
          '\n\n'\
          +total_request+\
          '------------------------------------\n'
    #create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((__HOST, __REMOTE_LOCAL))
    except OSError as msg:
        print('printing error \n'+msg)
        s.close()
        sys.exit(0)

    s.sendall(str(_TUNNELCODE))
    print('sent Tunnel ID: '+str(_TUNNELCODE))
    response = s.recv(1024)
    print('received response: '+response+'\n')

    server_communication(s, client_connection, client_address, total_request)

#####################################################################################################
def server_communication(server_socket, client_connection, client_address, initial_request):
    server_socket.sendall(initial_request)
    print('------------------------------------\n'
          'SENT actual request: '
          '\n\n'
          +initial_request+
          '-----------------------------------\n')

    is_readable = [server_socket, client_connection]
    is_writable = []
    is_error = []
    while True:
        r, w, e = select.select(is_readable, is_writable, is_error, 1.0)
        if r:
            for sock in r:
                if(sock == server_socket):
                    server_message = server_socket.recv(1024)
                    print('------------------------------------\n'
                        'NEW server message, Sent to client: '
                        '\n\n'
                        +server_message+
                        '-----------------------------------\n')
                    client_connection.sendall(server_message)
                else:
                    client_message = client_connection.recv(1024)
                    print('------------------------------------\n'
                        'NEW client message, Sent to server: '
                        '\n\n'
                        +client_message+
                        '-----------------------------------\n')
                    server_socket.sendall(client_message)
        # else:
        #     print "waiting for data to read"


#####################################################################################################
if __name__ == '__main__':
    print('Starting Client\' Agent')
    start_listening_client(__HOST, __CLIENT_LOCAL, __SERVER_LOCAL)