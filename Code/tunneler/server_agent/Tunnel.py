__author__ = 'cruiz1391'
from Client import Client

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

    def getTunnelId(self):
        return self.__myId

    def getTunnelConnection(self):
        return self.__myConnection

    def sendMessage(self, message):
        self.getTunnelConnection().sendall(message)

    def sendMessageToClient(self, clientId, message):
        self.__activeClients.get(clientId).sendMessage(message)
