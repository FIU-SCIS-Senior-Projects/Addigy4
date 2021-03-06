import inspect

__author__ = 'cruiz1391'
import sys, os, psutil, signal
import select
from ServerObject import Server
from LocalClient import Program
from ServerClient import Client
from socket import error as SocketError

TUNNEl_CLIENT_ID_SIZE = 36
DATA_SIZE_VALUE = 12
PORT_SIZE_VALUE = 32
BUFFER_SIZE = 2048

# HARDCODE_MYCODE = 'fc86c7ef-f579-4115-8137-289b8a257803'
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
    is_readable = [serverObject.getSocket()]
    is_writable = []
    is_error = []
    while True:
        try:
            r, w, e = select.select(is_readable, is_writable, is_error, 0)
        except KeyboardInterrupt:
            errMsg = "\nClient is being terminated by user!\nClosing connections..."
            fatalErrConnectionHandler(serverObject.getSocket(), errMsg)
            os._exit(0)
            return
        if r:
            for sock in r:
                if(sock == serverObject.getSocket()):
                    client_ID = readData(serverObject.getSocket(), TUNNEl_CLIENT_ID_SIZE)
                    if(len(client_ID) == 0):
                        sys.stderr.write("Server closed connection...")
                        os._exit(0)
                    ##if client does not exist
                    if(client_ID not in ACTIVE_SERVER_CLIENTS):
                        dest_port = readData(serverObject.getSocket(), PORT_SIZE_VALUE)
                        if(len(dest_port) == 0):
                            sys.stderr.write("Server closed connection...")
                            os._exit(0)
                        else:
                            # print('\n====================================================\n'
                            #         "New Client!"
                            #         "\nclient id: " +client_ID+
                            #         "\nlocal destination port: "+str(int(dest_port,2))
                            #         +'\n====================================================')
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
                        data_size = readData(serverObject.getSocket(), DATA_SIZE_VALUE)
                        serverMsg = readData(serverObject.getSocket(), int(data_size, 2))
                        if(len(data_size) == 0 or len(serverMsg) == 0):
                            del ACTIVE_SERVER_CLIENTS[client_ID]
                        else:
                            # print('\n====================================================\n'
                            #         "Received message from server"
                            #         "\nclient id: " + client_ID +
                            #         "\nto program: %08x" % id(ACTIVE_SERVER_CLIENTS[client_ID].getProgram()) +
                            #         "\nmessage: "+ str(serverMsg)
                            #         +'\n====================================================\n')
                            ACTIVE_SERVER_CLIENTS[client_ID].getProgram().sendMessage(serverMsg)
                else:
                    serverClient = serverClientsObjects[sock]
                    try:
                        programMsg = serverClient.getProgram().getSocket().recv(BUFFER_SIZE)
                    except SocketError:
                        errMsg = '\nProgram terminated connection!'
                        sys.stderr.write(errMsg)
                    programMsgSize = len(programMsg)
                    if(programMsgSize == 0):
                        sys.stderr.write("\nConnection closed by program!")
                        is_readable.remove(sock)
                        serverClient.getProgram().getSocket().close()
                        break
                    msgToSend = myId\
                                + serverClient.getId().encode() \
                                + bytes(bin(programMsgSize)[2:].zfill(DATA_SIZE_VALUE)) \
                                + programMsg
                    # print('\n====================================================\n'
                    #         "RECEIVED MESSAGE FROM PROGRAM"
                    #         "\nMESSAGE WILL BE SEND TO CLIENT: " + serverClient.getId() +
                    #         "\nMESSAGE SIZE: "+ str(len(programMsg)) +
                    #         "\nMESSAGE: \n"+ str(programMsg)
                    #         +'\n====================================================\n')
                    serverObject.getSocket().sendall(msgToSend)
#####################################################################################################
def fatalErrConnectionHandler(serverSocket, message):
    serverSocket.sendall(myId)
    sys.stderr.write('\n====================================================\n'
                    +message+
                    '\n====================================================\n')
#####################################################################################################
def errConnectionHandler(serverSocket, message):
    if(serverSocket != None):
        serverSocket.sendall(myId)
    sys.stderr.write('\n====================================================\n'
                    +message+
                    '\n====================================================\n')
#####################################################################################################
def startTunnelConnection(serverObject):
    # creste server object
    if(serverObject.connect()):
        serverObject.sendInitialMessage(myId)
        sys.stdout.write("Tunnel created: " + myId+"\n")
        sys.stdout.flush()
        serverMessageHandler(serverObject)
    else:
        os._exit(0)
###########################################################################################################
def readData(socket, dataSize):
    buf = b''
    while dataSize:
        newbuf = socket.recv(dataSize)
        if not newbuf: return ""
        buf += newbuf
        dataSize -= len(newbuf)
    return buf

#####################################################################################################
def tunnelExist():
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+"/Main.py"
    for p in psutil.process_iter():
        if(len(p.cmdline()) > 2 and str(p.cmdline()[1]) == str(path) and p.cmdline()[2] == myId and p.pid != os.getpid()):
            sys.stdout.write("Tunnel exist: " + myId+"\n")
            sys.stdout.flush()
            return True
    return False
#####################################################################################################
def signal_term_handler(signal, frame):
    serverObject.getSocket().close()
    sys.exit(0)
#####################################################################################################
if __name__ == '__main__':
    if(len(sys.argv) != 2):
        sys.stderr.write("\nIncorrect number of params <tunnel id>")
        sys.stderr.flush()
        sys.exit(0)
    if(len(sys.argv[1]) != TUNNEl_CLIENT_ID_SIZE):
        sys.stderr.write("\nIncorrect <tunnel id> size. needs to be 36bytes")
        sys.stderr.flush()
        sys.exit(0)
    global myId, serverObject
    myId = sys.argv[1]
    serverObject = Server()
    signal.signal(signal.SIGTERM, signal_term_handler)
    if(not tunnelExist()):
        startTunnelConnection(serverObject)
    else:
        sys.exit(0)
