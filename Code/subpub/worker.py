#!/usr/bin/env python
import pika
import time

__author__ = 'David Romero'

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)

print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    body = body.decode("utf-8")
    print(" [x] Received %r" % (body,))
    bodycount = body.count('.')
    time.sleep(bodycount)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='hello')

channel.start_consuming()
