from Queue import Queue
import traceback

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

# TUNNELS_DIC = {}
# TUNNELS_ON_SELECT = []


# List of all active sockets to receive information from
ACTIVE_SOCKETS = []
# dictionary key=socket, value client\tunnel object
SOCKETS_DICT = {}
# dictiory socket id to socket Key=id, value=client/tunnel object
SOCKETS_ID_DICT = {}
# queue for sockets that are ready to read from
READY_QUEUE = Queue()

##################################################################################################
##createsnew client and send its id to the desired tunnel and the target port number
def getClient(client_connection, client_address):
    client_id = dest_tunnel_id = dest_port = ""
    try:
        # receive <DESTINATION PORT> <DESTINATION TUNNEL ID> <CLIENT ID>
        dest_port = readData(client_connection, PORT_SIZE_VALUE)
        dest_tunnel_id = readData(client_connection, TUNNEl_CLIENT_ID_SIZE)
        client_id = readData(client_connection, TUNNEl_CLIENT_ID_SIZE)
    except SocketError:
        message = 'Client disconnected!'
        errConnectionHandler(client_connection, message)
    if(len(dest_port) == 0 or len(dest_port) == 0 or len(dest_port) == 0):
        message = 'Client disconnected!'
        errConnectionHandler(client_connection, message)
    if(client_id in SOCKETS_ID_DICT):
        return None
    # print("==========================================")
    # print("dest_port", int(dest_port, 2))
    # print("dest_tunnel_id", dest_tunnel_id)
    # print("client_id", client_id)
    # print("==========================================\n")
    ## prepare message to send to tunnel
    client_tunnel_handShake = client_id + bytes(dest_port)
    ## if the TUNNEL EXIST then send message
    ## ELSE
    ## respond back to client
    if(dest_tunnel_id in SOCKETS_ID_DICT):
        tunnel = SOCKETS_ID_DICT[dest_tunnel_id]
        tunnel.sendInitialMessage(client_tunnel_handShake)
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
    # print 'listening on port: %s ...' % __client_connection_port
    while True:
        try:
            client_connection, client_address = listen_client_socket.accept()
            # print("\nNew Client Connection!: " + client_address)
            newClient = getClient(client_connection, client_address)
            if(newClient != None):
                SOCKETS_ID_DICT[newClient.getId()] = newClient
                ACTIVE_SOCKETS.append(newClient.getConnection())
                SOCKETS_DICT[newClient.getConnection()] = newClient
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
    # print('listening on port: %s ...' % __tunnel_connection_port)
    while True:
        try:
            tunnel_connection, tunnel_address = listen_tunnel_socket.accept()
            print("\nNew Client Connection!: " + str(tunnel_address) + "--" +str(tunnel_connection._sock))
        except KeyboardInterrupt:
            message = "\nServer disconnecting!\nClosing connections..."
            errConnectionHandler(listen_tunnel_socket, message)
            sys.exit(0)
        try:
            # receiving tunnel uuid
            tunnel_id = readData(tunnel_connection, TUNNEl_CLIENT_ID_SIZE)
            if(tunnel_id in SOCKETS_ID_DICT):
                tunnel_connection.close()
            else:
                ## Create new tunnel
                newTunnel = Tunnel(tunnel_id, tunnel_connection)
                SOCKETS_ID_DICT[newTunnel.getId()] = newTunnel
                ACTIVE_SOCKETS.append(newTunnel.getTunnelConnection())
                SOCKETS_DICT[newTunnel.getTunnelConnection()] = newTunnel

                # print ('\n====================================================\n'
                #        "New tunnel connection established!"
                #        "\ntunnelID: "+ tunnel_id + ""
                #        "\nTunnelObject: %08x" % id(newTunnel)+
                #        '\n====================================================\n')
        except Exception as e:
            sys.stderr.write(str(e))
            traceback.print_exc()
##################################################################################################
def listenToActiveSockets():
    while True:
        try:
            is_writable = []
            is_error = []
            r, w, e = select.select(ACTIVE_SOCKETS, is_writable, is_error, 0)
            if r:
                for sock in r:
                    ACTIVE_SOCKETS.remove(sock)
                    socketObject = SOCKETS_DICT[sock]
                    READY_QUEUE.put(socketObject)
        except Exception as e:
            sys.stderr.write("size: "+str(len(ACTIVE_SOCKETS)))
            sys.stderr.write(str(e))
            traceback.print_exc()
##################################################################################################
def listenToReadyQueue():
    while True:
        try:
            socketObj = READY_QUEUE.get(block=True)
            value = socketObj.receive()
            if(value):
                ACTIVE_SOCKETS.append(socketObj.getSocket())
            else:
                raise Exception ("Socket connection closed")
        except Exception as e:
            del SOCKETS_DICT[socketObj.getSocket()]
            del SOCKETS_ID_DICT[socketObj.getId()]
            socketObj.cleanUp(ACTIVE_SOCKETS)
            sys.stderr.write(str(e))
            traceback.print_exc()
##################################################################################################
def errConnectionHandler(socket, message):
    socket.close()
    sys.stderr.write('\n====================================================\n'
                +message+
                '\n====================================================\n')
###########################################################################################################
def readData(socket, dataSize):
    buf = b''
    while dataSize:
        newbuf = socket.recv(dataSize)
        if not newbuf: return ""
        buf += newbuf
        dataSize -= len(newbuf)
    return buf
##################################################################################################
if __name__ == '__main__':
    # print('SERVER STARTING!!!')
    # listen to tunnels incoming DATA
    tunnels_on_select = Thread(target=initClientConnections, args=[__HOST, __client_connection_port])
    tunnels_on_select.daemon = True
    tunnels_on_select.start()
    # starting socket to listen for incoming connections from tunnels
    tunnelThread = Thread(target=initTunnelConnections, args=[__HOST, __tunnel_connection_port])
    tunnelThread.daemon = True
    tunnelThread.start()
    for i in range(1000):
        newThread =  Thread(target=listenToReadyQueue)
        newThread.daemon = True
        newThread.start()
    # listen to active sockets
    listenToActiveSockets()

