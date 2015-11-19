import shlex

__author__ = 'cruiz1391'

import json
import os, sys, traceback, subprocess
import pubsub

ChannelName = "DemoTest"
ServerAdd = 'addigy-dev.cis.fiu.edu'
ServerPort = 5672
PubSubId = "0c86c7ef-f579-4115-8137-289b8a257803"
connected = True
message = ""
###########################################################################################################
def receiveMessages(channel, method_frame, header_frame, body):
    try:
        jsonMssg = json.loads(body.decode("utf-8") )
        if(PubSubId in jsonMssg):
            request = jsonMssg[PubSubId]
            print("\nrequest received: " + str(request)+"\n")
            if(executeCommand(request)):
                print("success")
            else:
                print("failed")
    except ValueError as e:
        sys.stderr.write(str(e))
        traceback.print_exc()

###########################################################################################################
def subscribeToChannel():
    global pubSubClient
    pubSubClient = pubsub.PubSub(addr=ServerAdd, username='test2', password='test2')
    pubSubClient.subscribe(receiveMessages, ChannelName, no_ack=True)

###########################################################################################################
def startTunneler(tunnelId, path):
    print("starting tunneler!")
    command_line = "python " + path + " " + tunnelId
    args = shlex.split(command_line)
    if(not os.path.exists(path)):
        message = "Tunnel path doesn't exist!"
        return False
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    success = False
    while True:
        output = p.stdout.readline()
        if output == '' and p.poll() is not None:
            break
        if output:
            outputString = output.decode("utf-8")
            if(outputString == "Tunnel created: "+tunnelId+"\n" or outputString == "Tunnel exist: " + tunnelId+"\n"):
                success = True
                print (outputString)
                message = outputString
        if success:
            break
    if(success):
        return True
    else:
        return False

###########################################################################################################
def startClient(targetTunnel, localPort, destPort, path):
    print("starting client")
    command_line = "python " + path + " " + str(targetTunnel) + " " + str(localPort) + " " + str(destPort)
    args = shlex.split(command_line)
    if(not os.path.exists(path)):
        message = "Client path doesn't exist!"
        return False
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    success = False
    while True:
        output = p.stdout.readline()
        if output == '' and p.poll() is not None:
            break
        if output:
            outputString = output.decode("utf-8")
            if(outputString == "Client created: "+targetTunnel+"\n" or outputString == "Client exist: " + targetTunnel+"\n"):
                success = True
                print (outputString)
                message = outputString
        if success:
            break
    if(success):
        return True
    else:
        return False

###########################################################################################################
def executeCommand(request):
    PATH = "/var/opt/"
    target = request['target']
    try:
        if target == 'client':
            targetTunnel = request['tunnel_id']
            local_port = int(request['local_port'])
            connection_type = request['connection_type']
            return startClient(targetTunnel, local_port, portFromConnectionType(connection_type), PATH+"client/Main.py")
        elif target == 'tunneler':
            tunnelId = request['tunnel_id']
            return startTunneler(tunnelId, PATH+"tunneler/Main.py")
    except FileNotFoundError as error:
        sys.stderr.write(str(error))
        traceback.print_exc()
        return False

###########################################################################################################
def portFromConnectionType(connection_type):
    return{
        'web':80,
        'ssh':22,
        'vnc':4500,
    }.get(connection_type, -1)

###########################################################################################################
if __name__ == '__main__':
    subscribeToChannel()
