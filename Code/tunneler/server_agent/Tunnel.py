__author__ = 'cruiz1391'
from Client import Client

TUNNEl_CLIENT_ID_SIZE = 36
DATA_SIZE_VALUE = 12
PORT_SIZE_VALUE = 32

class Tunnel():
    __myId = ""
    __myConnection = None
    __activeClients = {}

    def __init__(self, id, connection):
        self.__myId = id
        self.__myConnection = connection

    def addClient(self, client):
        self.__activeClients[client.getId()] = client

    def getDestClientById(self, clientId):
        return self.__activeClients.get(clientId)

    def getId(self):
        return self.__myId

    def getTunnelConnection(self):
        return self.__myConnection

    def sendInitialMessage(self, message):
        self.__myConnection.sendall(message)

    def sendMessage(self, clientId, message):
        self.__myConnection.sendall(clientId+bytes(bin(len(message))[2:].zfill(DATA_SIZE_VALUE))+message)

    def getSocket(self):
        return self.getTunnelConnection()

    def receive(self):
        tunnelId = self.readData(TUNNEl_CLIENT_ID_SIZE)
        destClientId = self.readData(TUNNEl_CLIENT_ID_SIZE)
        if(len(destClientId) == 0):
            return False
        else:
            msgSize = self.readData(DATA_SIZE_VALUE)
            if(len(msgSize) > 0):
                tunnel_message = self.readData(int(msgSize,2))
                if(len(tunnel_message) == 0):
                    return False
                # print('\n====================================================\n'
                #     'destination client_id: '+destClientId+
                #     '\nNEW tunnel message Sent to client: '+tunnel_message+
                #     '\n====================================================\n')
                self.__activeClients[destClientId].sendMessage(tunnel_message)
                return True
            else:
                return False

    def readData(self, dataSize):
        buf = b''
        while dataSize:
            newbuf = self.__myConnection.recv(dataSize)
            if not newbuf: return ""
            buf += newbuf
            dataSize -= len(newbuf)
        return buf

    def cleanUp(self, ACTIVE_SOCKETS):
        for sockId in self.__activeClients.keys():
            # ACTIVE_SOCKETS.remove(self.__activeClients[sockId].getSocket())
            self.__activeClients[sockId].cleanUp(ACTIVE_SOCKETS)