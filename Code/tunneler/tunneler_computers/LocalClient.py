__author__ = 'cruiz1391'
import socket

class Program():
    __url = 'localhost'
    __port = 0
    __socket = None

    def __init__(self, port):
        self.__port = int(port, 2)

    def connect(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__socket.connect((self.__url, self.__port))
        except Exception as msg:
            self.__socket.close()
            return False
        return True

    def sendMessage(self, message):
        self.getSocket().sendall(message)

    def getSocket(self):
        return self.__socket
