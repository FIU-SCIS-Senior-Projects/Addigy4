__author__ = 'cruiz1391'
import sys, os
import select
from ServerObject import Server
from LocalClient import Program
from ServerClients import Client
from socket import error as SocketError

TUNNEl_CLIENT_ID_SIZE = 36
DATA_SIZE_VALUE = 12
PORT_SIZE_VALUE = 32
BUFFER_SIZE = 2048

HARDCODE_MYCODE = 'fc86c7ef-f579-4115-8137-289b8a257803'
_ACTIVE_SERVER_CLIENTS = {}

#####################################################################################################
def addNewClientAndOpenConnection(client_ID, portNumber):
    global __ACTIVE_CLIENTS_IDS
    __ACTIVE_CLIENTS_IDS.append(client_ID)
    newLocalProgram = Program(portNumber)
    if(not newLocalProgram.connect()):
        print("\nError connecting to port: "+str(portNumber))
    else:
        print("\nConnection opened port#: "+str(portNumber))
#####################################################################################################
def establishClientTunnelConnection(clientId, destPort):
    newProgram = Program(destPort)
    if(newProgram.connect()):
        newClient = Client(clientId, newProgram)
        return newClient
    else:
        print("\nCouldn't connect to local port at: " + str(int(destPort, 2)))
        return None

#####################################################################################################
def serverMessageHandler(serverObject):
    serverClientsObjects = {}
    serverSocket = serverObject.getSocket()
    is_readable = [serverSocket]
    is_writable = []
    is_error = []
    while True:
        try:
            r, w, e = select.select(is_readable, is_writable, is_error, 1.0)
        except KeyboardInterrupt:
            errMsg = "\nClient is being terminated by user!\nClosing connections..."
            fatalErrConnectionHandler(serverSocket, errMsg)
            os._exit(0)
            return
        if r:
            for sock in r:
                if(sock == serverSocket):
                    client_ID = serverSocket.recv(TUNNEl_CLIENT_ID_SIZE)
                    ##if client does not exist
                    if(client_ID not in _ACTIVE_SERVER_CLIENTS):
                        dest_port = serverSocket.recv(PORT_SIZE_VALUE)
                        if(len(client_ID) == 0 or len(dest_port) == 0):
                            print("Server closed connection...")
                            os._exit(0)
                        else:
                            print('\n====================================================\n'
                                    "New Client!"
                                    "\nclient id: " +client_ID+
                                    "\nlocal destination port: "+str(int(dest_port,2))
                                    +'\n====================================================')
                            newServerClient = establishClientTunnelConnection(client_ID, dest_port)
                            _ACTIVE_SERVER_CLIENTS[client_ID] = newServerClient
                            if(newServerClient == None):
                                print("\nClosing connection..")
                            else:
                                programSocket = newServerClient.getProgram().getSocket()
                                is_readable.append(programSocket)
                                serverClientsObjects[programSocket] = newServerClient
                    else:
                        ##If the client already exist
                        data_size = serverSocket.recv(DATA_SIZE_VALUE)
                        serverMsg = serverSocket.recv(int(data_size, 2))
                        print('\n====================================================\n'
                                "Received message from server"
                                "\nclient id: " + client_ID +
                                "\nto program: %08x" % id(_ACTIVE_SERVER_CLIENTS[client_ID].getProgram()) +
                                "\nmessage: "+ str(serverMsg)
                                +'\n====================================================\n')
                        _ACTIVE_SERVER_CLIENTS[client_ID].getProgram().getSocket().sendall(serverMsg)
                else:
                    serverClient = serverClientsObjects[sock]
                    try:
                        programMsg = sock.recv(BUFFER_SIZE)
                    except SocketError:
                        errMsg = 'Program terminated connection!'
                        errConnectionHandler(None, errMsg)
                    programMsgSize = len(programMsg)
                    if(programMsgSize == 0):
                        print("Connection closed by program!")
                        is_readable.remove(sock)
                        serverClient.getProgram().getSocket().close()
                        serverClient.getProgram().__del__()
                        serverClient.__del__()
                        break
                    msgToSend = HARDCODE_MYCODE\
                                + serverClient.getId().encode() \
                                + bytes(bin(programMsgSize)[2:].zfill(DATA_SIZE_VALUE)) \
                                + programMsg
                    print('\n====================================================\n'
                            "RECEIVED MESSAGE FROM PROGRAM"
                            "\nMESSAGE WILL BE SEND TO CLIENT: " + serverClient.getId() +
                            "\nMESSAGE SIZE: "+ str(len(programMsg)) +
                            "\nMESSAGE: \n"+ str(programMsg)
                            +'\n====================================================\n')
                    serverSocket.sendall(msgToSend)
#####################################################################################################
def fatalErrConnectionHandler(serverSocket, message):
    serverSocket.sendall(HARDCODE_MYCODE)
    print('\n====================================================\n'
            +message+
            '\n====================================================\n')
#####################################################################################################
def errConnectionHandler(serverSocket, message):
    if(serverSocket != None):
        serverSocket.sendall(HARDCODE_MYCODE)
    print('\n====================================================\n'
            +message+
            '\n====================================================\n')
#####################################################################################################
def startTunnelConnection(serverObject):
    # creste server object
    if(serverObject.connect()):
        serverObject.sendInitialMessage(HARDCODE_MYCODE)
        print('\n====================================================\n'
                "Tunnel created!"
                "\nTunnel id: " + HARDCODE_MYCODE
                +'\n====================================================\n')
        serverMessageHandler(serverObject)
    else:
        os._exit(0)

#####################################################################################################
if __name__ == '__main__':
    serverObject = Server()
    startTunnelConnection(serverObject)
