#!/usr/bin/env python
import pubsub_python
__author__ = 'David'

sample = pubsub_python.PubSub(addr='localhost', queue_name='hello')
message = input("Please enter your message: ")

while(True):
    channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
    print(" [x] Sent '%s!'" % (message,))

    if (message="exit"):
        sample.close()
