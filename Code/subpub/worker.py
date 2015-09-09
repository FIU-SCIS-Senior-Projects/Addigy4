#!/usr/bin/env python
import pika
import time

__author__ = 'David'

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    body = body.decode("utf-8")
    print(" [x] Received %r" % (body,))
    bodycount = body.count('.')
    time.sleep(bodycount)
    print(" [x] Done")

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

channel.start_consuming()
