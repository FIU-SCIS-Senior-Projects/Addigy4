__author__ = 'cruiz1391'
import uuid
import sys, os
import select
from socket import error as SocketError
from threading import *
from Client import *

TUNNEl_CLIENT_ID_SIZE = 36
DATA_SIZE_VALUE = 12
PORT_SIZE_VALUE = 32
BUFFER_SIZE = 2048

LOCALHOST = 'localhost'
#####################################################################################################
def ClientServerCommunication(client):
    myClient = client
    clientSocket = myClient.getConnection()
    serverSocket = myClient.getServerObject().getSocket()
    is_readable = [clientSocket, serverSocket]
    is_writable = []
    is_error = []
    while True:
        r, w, e = select.select(is_readable, is_writable, is_error, 1.0)
        if r:
            for sock in r:
                if(sock == serverSocket):
                    try:
                        serverMsgSize = serverSocket.recv(DATA_SIZE_VALUE)
                        if(len(serverMsgSize)==0):
                            message = 'Communication closed by program!\nClosing connections...'
                            errorConnectionHanlder(client, True, message)
                            return
                    except SocketError:
                        message = 'Communication closed by program!\nClosing connections...'
                        errorConnectionHanlder(client, True, message)
                        return

                    serverMsg = serverSocket.recv(int(serverMsgSize, 2))
                    print('\n====================================================\n'
                        'Message from server: '+serverMsg+
                        '\n====================================================\n')
                    clientSocket.sendall(serverMsg)
                else:
                    try:
                        clientMessage = clientSocket.recv(BUFFER_SIZE)
                        clientMsgSize = len(clientMessage)
                        if(clientMsgSize == 0):
                            message = 'Communication closed by program!\nClosing connections...'
                            errorConnectionHanlder(client, False,message)
                            return
                    except SocketError:
                        message = 'Communication closed by program!\nClosing connections...'
                        errorConnectionHanlder(client, False, message)
                        return

                    data_to_server = myClient.getDestTunnelId().encode() \
                                    + myClient.getId().__str__().encode() \
                                    + bytes(bin(clientMsgSize)[2:].zfill(DATA_SIZE_VALUE)) \
                                    + clientMessage
                    print('====================================================\n'
                        'NEW MESSAGE SENT TO SERVER: '
                        '\nTUNNEL ID: '+myClient.getDestTunnelId()+
                        '\n    MY ID: '+myClient.getId().__str__()+
                        '\nMESSAGE SIZE: '+str(clientMsgSize)+
                        '\nMESSAGE: \n'+str(clientMessage)+
                        '====================================================\n')
                    serverSocket.sendall(data_to_server)
        # else:
        #     print "waiting for data to read"
###########################################################################################################
def handleNewClientConnections(localPort, tunnelID, destPort):
    print("Listening at port: " + str(localPort))
    listen_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_client_socket.bind((LOCALHOST, localPort))
    listen_client_socket.listen(5)
    while True:
        ## new incoming client connection
        newClient = None
        try:
            client_connection, client_address = listen_client_socket.accept()
            my_id = uuid.uuid4()
            newClient = Client(my_id, client_connection, client_address)
        except KeyboardInterrupt:
            print("\nClient is being terminated by user!\nClosing connections...")
            listen_client_socket.close()
            print("bye!")
            os._exit(0)
        ## if connected to server return TRUE else FALSE
        if(newClient.connectToServer()):
            print("\nConnection established!")
            message = bytes(bin(destPort)[2:].zfill(PORT_SIZE_VALUE))\
                    + tunnelID\
                    + newClient.getId().__str__()
            newClient.setDestTunnelId(tunnelID)
            newClient.sendInitialMessage(message)

            ## new thread to handle communication
            ## client object and server object
            serverMsgHanlderThread = Thread(target=ClientServerCommunication, args=[newClient])
            serverMsgHanlderThread.daemon = True
            serverMsgHanlderThread.start()
        else:
            newClient.getConnection().sendall("Error: Couldn't connect to server!\n")
            newClient.getConnection().close()
###########################################################################################################
def setupClient(params):
    print("STARTING UP CLIENT...")
    tunnelID = params[1]
    localPort = int(params[2])
    destPort = int(params[3])
    print('\n====================================================\n'
            'param1: '+tunnelID+
            '\nparam2: '+str(localPort)+
            '\nparam3: '+str(destPort)+
            '\n====================================================\n')
    handleNewClientConnections(localPort, tunnelID, destPort)

###########################################################################################################
def errorConnectionHanlder(clientSocket, isServerErr, message):
    print(message)
    if isServerErr:
        clientSocket.getConnection().sendall("Error: Couldn't connect to server!\n")
    clientSocket.getConnection().close()
    clientSocket.getServerObject().getSocket().close()
    clientSocket.__del__()
    return True
###########################################################################################################
if __name__ == '__main__':
    if(len(sys.argv) != 4):
        print("\nIncorrect number of params <tunnel id> <local port> <destination port>")
        sys.exit(0)
    else:
        setupClient(sys.argv)