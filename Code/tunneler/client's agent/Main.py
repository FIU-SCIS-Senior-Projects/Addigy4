__author__ = 'cruiz1391'
import sys
import socket


__HTTP_LOCAL = 5000
__SERVER_LOCAL = 7000
__HOST = 'localhost'
_TUNNELCODE = 999999

def start_listening_http(__HOST, __HTTP_LOCAL, __SERVER_LOCAL):
    listen_http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_http_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_http_socket.bind((__HOST, __HTTP_LOCAL))
    listen_http_socket.listen(5)
    print 'listening %s ...' % __HTTP_LOCAL
    while True:
        client_connection, client_address = listen_http_socket.accept()
        request = client_connection.recv(1000000)
        print '------------------------------------\n' \
              'Request from HTTP:' \
              '\n\n'\
              +request+\
              '------------------------------------\n'
        if("GET /favicon.ico" in request):
            print("IGNORING FAVICON FOR NOW")
        else:
            response = connect_server(__HOST, __SERVER_LOCAL, request)
            client_connection.sendall(response)

def connect_server(__HOST, __REMOTE_LOCAL, myRequest):
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
    response = s.recv(1000000)
    print('received response: '+response+'\n')

    s.sendall(myRequest+"\n")
    print('------------------------------------\n'
          'SENT actual request: '
          '\n\n'
          +myRequest+
          '-----------------------------------\n')

    data = (s.recv(1000000))
    print('------------------------------------\n'
          'RECEIVED final response:'
          '\n\n'
          +data+
          "-----------------------------------\n")
    return data



if __name__ == '__main__':
    print('Starting Client\' Agent')
    start_listening_http(__HOST, __HTTP_LOCAL, __SERVER_LOCAL)