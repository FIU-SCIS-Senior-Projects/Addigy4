#!/usr/bin/env python
import sys
import pika
__author__ = 'David Romero'

# Establishing a connection with the RabbitMq server. IN this case the broker is on
# the local machine, hence 'localhost'
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

# We need to make sure the recipient queue exists. We create a queue to which the messgae
# to which the message will be delivered
channel.queue_declare(queue='hello', durable=True)

# Sending the message! No exchange server specified, message place in hello queue. The message
# sent is "Hello world"

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2,
                      ))


print(" [x] Sent %r" % (message,))


# Make sure the network buffers were flushed and our message was actually delivered
# by gently closing the connection
connection.close()


