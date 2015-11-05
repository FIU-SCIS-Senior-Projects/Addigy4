__author__ = 'cruiz1391'

from LocalClient import *
class Client():
    __id = None
    __program = None

    def __init__(self, clientId, program):
        self.__id = clientId
        self.__program = program

    def getProgram(self):
        return self.__program

    def getId(self):
        return self.__id
