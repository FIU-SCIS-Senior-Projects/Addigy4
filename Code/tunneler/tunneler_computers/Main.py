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
ACTIVE_SERVER_CLIENTS = {}

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
        sys.stderr.write("\nCouldn't connect to local port at: " + str(int(destPort, 2)))
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
                    if(client_ID not in ACTIVE_SERVER_CLIENTS):
                        dest_port = readData(serverSocket, PORT_SIZE_VALUE)
                        if(len(client_ID) == 0 or len(dest_port) == 0):
                            sys.stderr.write("Server closed connection...")
                            os._exit(0)
                        else:
                            print('\n====================================================\n'
                                    "New Client!"
                                    "\nclient id: " +client_ID+
                                    "\nlocal destination port: "+str(int(dest_port,2))
                                    +'\n====================================================')
                            newServerClient = establishClientTunnelConnection(client_ID, dest_port)
                            ACTIVE_SERVER_CLIENTS[client_ID] = newServerClient
                            if(newServerClient == None):
                                sys.stderr.write("\nClosing connection..")
                            else:
                                programSocket = newServerClient.getProgram().getSocket()
                                is_readable.append(programSocket)
                                serverClientsObjects[programSocket] = newServerClient
                    else:
                        ##If the client already exist
                        data_size = readData(serverSocket, DATA_SIZE_VALUE)
                        serverMsg = readData(serverSocket, int(data_size, 2))
                        if(len(data_size) == 0 or len(serverMsg) == 0):
                            sys.stderr.write("Server closed connection...")
                            os._exit(0)
                        print('\n====================================================\n'
                                "Received message from server"
                                "\nclient id: " + client_ID +
                                "\nto program: %08x" % id(ACTIVE_SERVER_CLIENTS[client_ID].getProgram()) +
                                "\nmessage: "+ str(serverMsg)
                                +'\n====================================================\n')
                        ACTIVE_SERVER_CLIENTS[client_ID].getProgram().getSocket().sendall(serverMsg)
                else:
                    serverClient = serverClientsObjects[sock]
                    try:
                        programMsg = sock.recv(BUFFER_SIZE)
                    except SocketError:
                        errMsg = 'Program terminated connection!'
                        sys.stderr.write(errMsg)
                    programMsgSize = len(programMsg)
                    if(programMsgSize == 0):
                        sys.stderr.write("Connection closed by program!")
                        is_readable.remove(sock)
                        serverClient.getProgram().getSocket().close()
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
    sys.stderr.write('\n====================================================\n'
                    +message+
                    '\n====================================================\n')
#####################################################################################################
def errConnectionHandler(serverSocket, message):
    if(serverSocket != None):
        serverSocket.sendall(HARDCODE_MYCODE)
    sys.stderr.write('\n====================================================\n'
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
###########################################################################################################
def readData(socket, dataSize):
    dataToReturn = ""
    dataRead = ""
    dataReadLength = 0
    while (dataReadLength != dataSize):
        dataRead=socket.recv(dataSize-dataReadLength)
        dataReadLength += len(dataRead)
        if(len(dataRead)==0):
            return ""
        dataToReturn += dataRead
    return dataRead
#####################################################################################################
if __name__ == '__main__':
    serverObject = Server()
    startTunnelConnection(serverObject)
