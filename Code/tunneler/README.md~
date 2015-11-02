#Tunneler:
	- Project is intended to establish a connection between two clients using a middle server.
	- Three piece of software are going to be needed:
		- Client: which is going to be used in machines that are going to initialize connections
		- Tunneler: Which is going to be installed on machines where the user wants to connect to
		- Server: which is going to be running on the server redirecting each data message received to intended recipient

##Installation:
	1) Server needs to be uploaded to a web services such as AWS and ports 7000 and 8000 has to be 		   opened.
	2) Client needs to be downloaded into the machine which will initialize connection. 
	3) Tunneler needs to be downloaded into the end point machine (machine the user is going to   		   connect to).
	4) Client and Tunnel boths will have to be updated:
		- open their directory and navigate to "ServerObject.py"
		- find "def __init__(self):" and update "self.__url" with the url where the Server is 			  going to be running
		- save and exit

##Running:
	1) Server must be running.
	2) Start Tunneler and connect to server. [params tunnelId(needs to be 36 byte id)]
	3) Start client and connect to server. [params (destination_tunnel_id, local port, destination 		   port)]
	4) Open intended service (Web, ssh, vnc), connect to Client using:
		- address: "localhost"
		- local port: "local port given on step 3"
