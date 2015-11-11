__author__ = 'cruiz1391'
from pubsub import *


ChannelName = "DemoTest"
ServerAdd = 'addigy-dev.cis.fiu.edu'
ServerPort = 5672
PubSubId = "0c86c7ef-f579-4115-8137-289b8a257803"
###########################################################################################################
def receiveMessages():
    messageReceived = pubSubClient.get_messageexchange()
    print(messageReceived)
###########################################################################################################
def subscribeToChannel():
    global pubSubClient
    pubSubClient = PubSub(addr=ServerAdd, port=ServerPort)
    pubSubClient.subscribe(receiveMessages, ChannelName)
###########################################################################################################
if __name__ == '__main__':
    subscribeToChannel()