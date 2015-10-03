__author__ = 'cruiz1391'
import sys, os
import socket
import select
from Tunnel import *
from threading import Thread
from socket import error as SocketError


__tunnel_connection_port = 8000
__client_connection_port = 7000
__HOST = 'localhost'

TUNNEl_CLIENT_ID_SIZE = 36
DATA_SIZE_VALUE = 12
PORT_SIZE_VALUE = 32

TUNNELS_DIC = {}
TUNNELS_ON_SELECT = []


##################################################################################################
def clientMessageHandler(client):
    clientSocket = client.getConnection()
    is_readable = [client.getConnection()]
    is_writable = []
    is_error = []
    keepLoop = True
    while keepLoop:
        r, w, e = select.select(is_readable, is_writable, is_error)
        if r:
            print("New message from client!")
            tunnel_dest_id = clientSocket.recv(TUNNEl_CLIENT_ID_SIZE)
            if(len(tunnel_dest_id) == 0):
                print("Connection closed by client!\nClosing connection...")
                client.getConnection().close()
                keepLoop = False
            else:
                client_id = clientSocket.recv(TUNNEl_CLIENT_ID_SIZE)
                data_size = clientSocket.recv(DATA_SIZE_VALUE)
                client_message = clientSocket.recv(int(data_size,2))
                print('====================================================\n'
                    'NEW MESSAGE FROM CLIENT: '
                    '\ntunnel_dest_id: '+tunnel_dest_id+
                    '\n     client_id: '+client_id+
                    '\ndata_size: '+str(int(data_size, 2))+
                    '\nclient_message: '+client_message+
                    '\n====================================================\n')

                TUNNELS_DIC[tunnel_dest_id].sendMessage(client_id+bytes(data_size)+client_message)
        # else:
        #     print "waiting for data to read"
##################################################################################################
def tunnelMessageHandler():
    print("listening to tunnels on select......")
    while True:
        is_writable = []
        is_error = []
        r, w, e = select.select(TUNNELS_ON_SELECT, is_writable, is_error, 1.0)
        if r:
            for sock in r:
                tunnelId = sock.recv(TUNNEl_CLIENT_ID_SIZE)
                destClientId = sock.recv(TUNNEl_CLIENT_ID_SIZE)
                if(len(destClientId) == 0):
                    print('closing tunnel connection...')
                    TUNNELS_ON_SELECT.remove(sock)
                    if(tunnelId in TUNNELS_DIC):
                        TUNNELS_DIC.pop(tunnelId)
                    sock.close()
                else:
                    msgSize = sock.recv(DATA_SIZE_VALUE)
                    tunnel_message = ""
                    if(len(msgSize) > 0):
                        tunnel_message = sock.recv(int(msgSize,2))
                        print('\n====================================================\n'
                            'destination client_id: '+destClientId+
                            '\nNEW tunnel message Sent to client: '+tunnel_message+
                            '\n====================================================\n')
                        tunnelObject = TUNNELS_DIC[tunnelId]
                        tunnelObject.sendMessageToClient(destClientId, tunnel_message)
        # else:vevo 2015
        #     print "waiting for data to read"
##################################################################################################
##createsnew client and send its id to the desired tunnel and the target port number
def getClient(client_connection, client_address):
    client_id = dest_tunnel_id = dest_port = ""
    try:
        # receive <DESTINATION PORT> <DESTINATION TUNNEL ID> <CLIENT ID>
        dest_port = client_connection.recv(PORT_SIZE_VALUE)
        dest_tunnel_id = client_connection.recv(TUNNEl_CLIENT_ID_SIZE)
        client_id = client_connection.recv(TUNNEl_CLIENT_ID_SIZE)
    except SocketError:
        message = 'Client disconnected!'
        errConnectionHandler(client_connection, message)
    if(len(dest_port) == 0 or len(dest_port) == 0 or len(dest_port) == 0):
        message = 'Client disconnected!'
        errConnectionHandler(client_connection, message)
    print("==========================================")
    print("dest_port", int(dest_port, 2))
    print("dest_tunnel_id", dest_tunnel_id)
    print("client_id", client_id)
    print("==========================================\n")
    ## prepare message to send to tunnel
    client_tunnel_handShake = client_id + bytes(dest_port)
    ## if the TUNNEL EXIST then send message
    ## ELSE
    ## respond back to client
    if(dest_tunnel_id in TUNNELS_DIC):
        tunnel = TUNNELS_DIC[dest_tunnel_id]
        tunnel.sendMessage(client_tunnel_handShake)
        return Client(client_id, client_connection, client_address, tunnel)
    else:
        errResponse = "Tunnel id doesnt exist!\n"
        client_connection.sendall(bytes(bin(len(errResponse))[2:].zfill(DATA_SIZE_VALUE))+errResponse)
        return None
##################################################################################################
def initClientConnections(__HOST, __client_connection_port):
    listen_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_client_socket.bind((__HOST, __client_connection_port))
    listen_client_socket.listen(5)
    print 'listening on port: %s ...' % __client_connection_port
    while True:
        try:
            client_connection, client_address = listen_client_socket.accept()
            print("\nNew Client Connection!")
            newClient = getClient(client_connection, client_address)
            if(newClient != None):
                client_thread = Thread(target=clientMessageHandler, args=[newClient])
                client_thread.daemon = True
                client_thread.start()
            else:
                client_connection.close()
        except KeyboardInterrupt:
            print("\nServer disconnecting!\nClosing connections...")
            os._exit(0)
##################################################################################################
def initTunnelConnections(__HOST, __tunnel_connection_port):
    listen_tunnel_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_tunnel_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_tunnel_socket.bind((__HOST, __tunnel_connection_port))
    listen_tunnel_socket.listen(5)
    print('listening on port: %s ...' % __tunnel_connection_port)
    while True:
        try:
            tunnel_connection, tunnel_address = listen_tunnel_socket.accept()
        except KeyboardInterrupt:
            message = "\nServer disconnecting!\nClosing connections..."
            errConnectionHandler(listen_tunnel_socket, message)
            sys.exit(0)
        # receiving tunnel uuid
        tunnel_id = tunnel_connection.recv(TUNNEl_CLIENT_ID_SIZE)
        ## Create new tunnel
        newTunnel = Tunnel(tunnel_id, tunnel_connection)

        #add tunnel to list of tunnles to listen tunnels_on_select
        if(tunnel_id in TUNNELS_DIC):
            del TUNNELS_DIC[tunnel_id]
        TUNNELS_DIC[tunnel_id] = newTunnel
        if(newTunnel.getTunnelConnection() in TUNNELS_ON_SELECT):
            TUNNELS_ON_SELECT.remove(newTunnel.getTunnelConnection())
        TUNNELS_ON_SELECT.append(newTunnel.getTunnelConnection())

        print ('\n====================================================\n'
               "New tunnel connection established!"
               "\ntunnelID: "+ tunnel_id + ""
               "\nTunnelObject: %08x" % id(newTunnel)+
               '\n====================================================\n')
##################################################################################################
def errConnectionHandler(socket, message):
    socket.close()
    print('\n====================================================\n'
            +message+
            '\n====================================================\n')
##################################################################################################
if __name__ == '__main__':
    print('SERVER STARTING!!!')
    # listen to tunnels incoming DATA
    tunnels_on_select = Thread(target=tunnelMessageHandler)
    tunnels_on_select.daemon = True
    tunnels_on_select.start()
    # starting socket to listen for incoming connections from tunnels
    tunnelThread = Thread(target=initTunnelConnections, args=[__HOST, __tunnel_connection_port])
    tunnelThread.daemon = True
    tunnelThread.start()
    # listen for incoming client connections
    initClientConnections(__HOST, __client_connection_port)
