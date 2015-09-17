__author__ = 'cruiz1391'
import socket
import sys
import select
from threading import Thread

host = 'localhost'
server_port = 8000
local_port = 22
BUFFER_ZISE = 1024
HARDCODE_MYCODE = 999999

#####################################################################################################
# def connect_local_webhost(data):
#     #create a socket object
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     try:
#         s.connect((host, local_port))
#     except OSError as msg:
#         print(msg)
#         s.close()
#         sys.exit(0)
#     s.sendall(data)
#     total = ""
#     data = None
#     # while data is None or len(data) != 0:
#     #     data = s.recv(1024)
#     #     total += data
#     total = s.recv(1000000)
#     print 'received from local server\n'+total
#     s.shutdown(1)
#     s.close()
#     return total

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
    tunnel_socket.sendall(str(HARDCODE_MYCODE))
    created_response = tunnel_socket.recv(1024)
    print(created_response)

    tunnel_thread = Thread(target=tunnel_communication, args=[tunnel_socket])
    tunnel_thread.start()

def tunnel_communication(tunnel_socket):
    #create a socket object
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    first_message = True

    is_readable = [tunnel_socket]
    is_writable = []
    is_error = []
    while True:
        r, w, e = select.select(is_readable, is_writable, is_error, 1.0)
        if r:
            for sock in r:
                if(sock == tunnel_socket):
                    tunnel_message = tunnel_socket.recv(1024)
                    print('------------------------------------\n'
                        'NEW tunnel message, Sent to local_socket: '
                        '\n\n'
                        +tunnel_message+
                        '-----------------------------------\n')

                    if(first_message):
                        first_message = False
                        try:
                            local_socket.connect((host, local_port))
                        except OSError as msg:
                            print(msg)
                            local_socket.close()
                            sys.exit(0)
                        is_readable.append(local_socket)

                    local_socket.sendall(tunnel_message)
                else:
                    local_message = local_socket.recv(1024)
                    if(len(local_message)>0):
                        print('------------------------------------\n'
                            'NEW client message, Sent to server: '
                            '\n\n'
                            +local_message+
                            '-----------------------------------\n')
                        tunnel_socket.sendall(local_message)
        # else:
        #     print "waiting for data to read"

#####################################################################################################
if __name__ == '__main__':
    create_tunnel_connection()
