#!/usr/bin/env python
import pika
__author__ = 'David'

# Establishing a connection with the RabbitMq server. IN this case the broker is on
# the local machine, hence 'localhost'
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

# We need to make sure the recipient queue exists. We create a queue to which the messgae
# to which the message will be delivered
channel.queue_declare(queue='hello')

# Sending the messsage! No exchange server specified, message place in hello queue. The message
# sent is "Hello world"
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

# Make sure the network buffers were flushed and our message was actually delivered
# by gently closing the connection
connection.close()
