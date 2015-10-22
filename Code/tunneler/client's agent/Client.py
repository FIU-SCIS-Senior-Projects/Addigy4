__author__ = 'cruiz1391'

from ServerObject import *
from Main  import PORT_SIZE_VALUE

class Client():
    __id = None
    __socket = None
    __address = None
    __serverObject = None
    __destTunnelId = ""

    def __init__(self, clientId, myConnection, myAddress):
        self.__id = clientId
        self.__socket = myConnection
        self.__address = myAddress
        self.__serverObject = Server()
        self.__serverObject.setClient(self)

    def setDestTunnelId(self, tunnelId):
        self.__destTunnelId = tunnelId

    def getDestTunnelId(self):
        return self.__destTunnelId

    def connectToServer(self):
        return self.__serverObject.connect()

    def getServerObject(self):
        return self.__serverObject

    def getId(self):
        return self.__id

    def getConnection(self):
        return self.__socket

    def getAddress(self):
        return self.__address

    def sendInitialMessage(self, message):
        self.getServerObject().sendMessage(message)
