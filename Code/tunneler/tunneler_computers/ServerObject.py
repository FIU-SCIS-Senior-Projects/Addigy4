__author__ = 'cruiz1391'
import socket


class Server():
    __serverPort = 0
    __url = ""
    __socket = None

    def __init__(self):
        self.__serverPort = 8000
        self.__url = 'fiu.addigy.com'
        return

    def connect(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__socket.connect((self.__url, self.__serverPort))
        except Exception as msg:
            print("\nCouldn't connect to server...\nPlease try again!")
            self.__socket.close()
            return False
        return True

    def sendInitialMessage(self, tunnelId):
        self.getSocket().sendall(tunnelId)

    def setToClientID(self, clientID):
        self.__toClientId = clientID

    def getSocket(self):
        return self.__socket
