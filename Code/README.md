#Addigy project has two goals:

## Tunneler:
	- Project is intended to establish a connection between two clients using a middle server.
	- Three piece of software are going to be needed:
		- Client: which is going to be used in machines that are going to initialize connections
		- Tunneler: Which is going to be installed on machines where the user wants to connect to
		- Server: which is going to be running on the server redirecting each data message received to intended recipient

## PubSub:
    - Any client implementing this class will be able to communicated with a RabbitMQ AMQP broker
    - For the sake of simplicity and time the PubSub class at the moment will be able to perform four crucial functions
        - Connect: The client using the class will be able to establish a connection to RabbitMQ broker server
        - Publish: The client using the class will be able to publish a message to any given queue that exists in the server
        - Subscribe: The client using the class will be able to consume the published message
        - Disconnect: Terminate the connection to the server
