#Tunneler:
	- Project is intended to establish a connection between two clients using a middle server.
	- Three piece of software are going to be needed:
		- Client: which is going to be used in machines that are going to initialize connections
		- Tunneler: Which is going to be installed on machines where the user wants to connect to
		- Server: which is going to be running on the server redirecting each data message received to intended recipient
		- Webhost Local is a simple web server for testing purposes of accessing a tunnel with a running server for web access.

		(Demo purpose)
		- Pubsub Agent: is going to be install in every machine as an intermidiate program which will start and terminate each service

##Installation:
	1) Download all github project
	2) Go to downloaded file and proceed into Code/Tunneler 
	3) for each available dir enter and run setup.sh file except for Server which will be install on AWS or similar.
	4) Server needs to be uploaded to a web services such as AWS and ports 8500 and 8000 has to be opened, then run setup.s file.
	7) Client and Tunnel boths will have to be updated:
		- open their directory and navigate to "ServerObject.py"
		- find "def __init__(self):" and update "self.__url" with the url where the Server is going to be running
		- save and exit

##Running:
	1) Server must be running.
	2) Start Tunneler and connect to server. [params tunnelId(needs to be 36 byte id)]
	3) Start client and connect to server. [params (destination_tunnel_id, local port, destination port)]
	4) Open intended service (Web, ssh, vnc), connect to Client using:
		- address: "localhost"
		- local port: "local port given on step 3"

##Demo presentation
	1) Server must be running
	2) Start pubsub agent on two machines and connect as a valid user.(Different account for each machine)
		- Before running pubsub aget:
			- Open on PyCharm or any other python IDE
			- Locate top variable "PubSubId"
			- On one machine this id mut start with '0' and on the oher with '1'
			- Locate variable "usrnANDpassw"
			- On one machine should be "test4" and on the other "test5"
			- Locate variable "queueName"
			- On one machine should be "test4_mailbox" and on the other "test5_mailbox"
			- Save and exit
		- Run program on each machine
		
	
