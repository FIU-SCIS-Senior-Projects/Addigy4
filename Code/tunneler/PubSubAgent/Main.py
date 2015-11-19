import shlex
import getpass
from threading import Thread
import webbrowser

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

usrnANDpassw = "test4"
queueName = "test4_mailbox"
routingKey = "testcorp"
###########################################################################################################
def failedAction():
    return False
###########################################################################################################
def startSSH(command):
    os.system("gnome-terminal -e 'bash -c \"%s; exec bash\"'" % command)
###########################################################################################################
def startWEB(url):
    webbrowser.open_new(url)
###########################################################################################################
def startVNC(port):
    os.system("vncviewer localhost:"+port)
###########################################################################################################
def successAction(request):
    target = request['target']
    if target == 'client':
        connection = request['connection_type']
        if(connection == "ssh"):
            print("opening terminal!")
            command = "ssh -v "+getpass.getuser()+"@localhost -p "+request['local_port']
            tunnels_on_select = Thread(target=startSSH, args=[command])
            tunnels_on_select.daemon = True
            tunnels_on_select.start()
        elif(connection == "web"):
            print("opening browser!")
            url = "http://localhost:3000"
            tunnels_on_select = Thread(target=startWEB, args=[url])
            tunnels_on_select.daemon = True
            tunnels_on_select.start()
        elif(connection == "vnc"):
            print("opening vnc!")
            port = request['local_port']
            tunnels_on_select = Thread(target=startVNC, args=[port])
            tunnels_on_select.daemon = True
            tunnels_on_select.start()
    elif target == 'tunneler':
        successResponse = request['messageToClient']
        pubSubClient.publish(routing_key=routingKey, body=bytes(json.dumps(successResponse), 'utf-8'))
###########################################################################################################
def receiveMessages(channel, method_frame, header_frame, body):
    try:
        jsonMssg = json.loads(body.decode("utf-8") )
        if(PubSubId in jsonMssg):
            request = jsonMssg[PubSubId]
            print("\nrequest received: " + str(request)+"\n")
            if(executeCommand(request)):
                print("success")
                successAction(request)
            else:
                print("failed")
    except ValueError as e:
        # Sring is not a valid json format text
        # do nothin
        sys.stderr.write("Message not a valid Json: " + body.decode("utf-8")+"\n")

###########################################################################################################
def subscribeToChannel():
    global pubSubClient
    pubSubClient = pubsub.PubSub(addr=ServerAdd, username=usrnANDpassw, password=usrnANDpassw, organization=routingKey)
    pubSubClient.create_queue(queue_name=queueName, auto_delete=True)
    pubSubClient.subscribe(receiveMessages, queueName, no_ack=True)

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
            tunnelport = request['tunnel_port']
            return startClient(targetTunnel, local_port, tunnelport, PATH+"client/Main.py")
        elif target == 'tunneler':
            tunnelId = request['tunnel_id']
            return startTunneler(tunnelId, PATH+"tunneler/Main.py")
    except FileNotFoundError as error:
        sys.stderr.write(str(error))
        traceback.print_exc()
        return False
###########################################################################################################
if __name__ == '__main__':
    subscribeToChannel()
