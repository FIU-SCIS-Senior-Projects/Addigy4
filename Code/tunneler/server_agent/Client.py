import sys

__author__ = 'cruiz1391'

from Tunnel import *
from Main  import PORT_SIZE_VALUE

TUNNEl_CLIENT_ID_SIZE = 36
DATA_SIZE_VALUE = 12
PORT_SIZE_VALUE = 32

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
        self.__tunnelObject.addClient(self)

    def getId(self):
        return self.__id

    def getConnection(self):
        return self.__socket

    def getSocket(self):
        return self.getConnection()

    def getAddress(self):
        return self.__address

    def getTunnelObject(self):
        return self.__tunnelObject

    def sendMessage(self, message):
        self.__socket.sendall(bytes(bin(len(message))[2:].zfill(self.DATA_SIZE_VALUE))+message)

    def receive(self):
        # print("New message from client!")
        tunnel_dest_id = self.readData(TUNNEl_CLIENT_ID_SIZE)
        if(len(tunnel_dest_id) == 0):
            sys.stderr.write("Connection closed by client!\nClosing connection...")
            self.__tunnelObject.sendMessage(self.__id, "")
            return False
        else:
            client_id = self.readData(TUNNEl_CLIENT_ID_SIZE)
            if(len(client_id) == 0):
                self.__tunnelObject.sendMessage(self.__id, "")
                return False
            data_size = self.readData(DATA_SIZE_VALUE)
            if(len(data_size) == 0):
                self.__tunnelObject.sendMessage(self.__id, "")
                return False
            client_message = self.readData(int(data_size,2))
            if(len(client_message) == 0):
                self.__tunnelObject.sendMessage(self.__id, "")
                return False
            # print('====================================================\n'
            #     'NEW MESSAGE FROM CLIENT: '
            #     '\ntunnel_dest_id: '+tunnel_dest_id+
            #     '\n     client_id: '+client_id+
            #     '\ndata_size: '+str(int(data_size, 2))+
            #     '\nclient_message: '+client_message+
            #     '\n====================================================\n')

            self.__tunnelObject.sendMessage(client_id, client_message)
            return True

    def readData(self, dataSize):
        buf = b''
        while dataSize:
            newbuf = self.__socket.recv(dataSize)
            if not newbuf: return ""
            buf += newbuf
            dataSize -= len(newbuf)
        return buf

    def cleanUp(self):
        try:
            self.__socket.close()
        except Exception as e:
            sys.stderr.write(str(e))