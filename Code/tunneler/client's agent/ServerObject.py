__author__ = 'cruiz1391'

import socket
from Client import *

class Server():
    __socket = None
    __serverPort = 0
    __url = ""


    def __init__(self):
        self.__serverPort = 7000
        self.__url = 'localhost'

    def connect(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__socket.connect((self.__url, self.__serverPort))
        except Exception as msg:
            print("\nCouldn't connect to server...\nPlease try again!")
            self.__socket.close()
            return False
        return True

    def setClient(self, client):
        self.__talkingToClient = client

    def getClient(self):
        return self.__talkingToClient

    def getSocket(self):
        return self.__socket

    def sendMessage(self, message):
        print('Initial message sent to server <destination port> <destination tunnel id> <client id>'
            '\n====================================================\n'
                'SERVER OBJECT: %08x ' % id(self.__talkingToClient) +
                'SENT: <destination port> <destination tunnel id> <client id>\n'
                'SENT: '+ message+
            '\n====================================================\n')
        self.getSocket().sendall(message)

    def __del__(self):
        print ("__del__() called: server object %08x destroyed" % id(self))