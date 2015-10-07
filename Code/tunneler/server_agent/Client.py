__author__ = 'cruiz1391'

from Tunnel import *
from Main  import PORT_SIZE_VALUE

class Client():
    __id = None
    __socket = None
    __address = None
    __tunnelObject = None
    DATA_SIZE_VALUE = 12

    def __init__(self, myId, mySocket, myAddress, tunnelObject):
        self.__id = myId
        self.__socket = mySocket
        self.__address = myAddress
        self.__tunnelObject = tunnelObject
        tunnelObject.addClient(self)

    def getId(self):
        return self.__id

    def getConnection(self):
        return self.__socket

    def getAddress(self):
        return self.__address

    def getTunnelObject(self):
        return self.__tunnelObject

    def sendMessage(self, message):
        self.__socket.sendall(bytes(bin(len(message))[2:].zfill(self.DATA_SIZE_VALUE))+message)
