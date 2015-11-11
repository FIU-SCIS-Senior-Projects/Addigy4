__author__ = 'cruiz1391'

import traceback
import socket
import sys
from Client import *

class Server():
    __socket = None
    __serverPort = 0
    # addigy-dev.cis.fiu.edu        fiu server
    # fiu.addigy.com                jason server
    __url = "fiu.addigy.com"


    def __init__(self):
        self.__serverPort = 7000
        self.__url = 'addigy-dev.cis.fiu.edu'

    def connect(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__socket.connect((self.__url, self.__serverPort))
        except Exception as msg:
            tb = traceback.format_exc()
            sys.stderr.write(tb)
            sys.stderr.write("\nCouldn't connect to server...\nPlease try again!")
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
        # print('Initial message sent to server <destination port> <destination tunnel id> <client id>'
        #     '\n====================================================\n'
        #         'SERVER OBJECT: %08x ' % id(self.__talkingToClient) +
        #         'SENT: <destination port> <destination tunnel id> <client id>\n'
        #         'SENT: '+ message+
        #     '\n====================================================\n')
        self.getSocket().sendall(message)
