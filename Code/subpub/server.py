#!/usr/bin/env python
import pika
import os

__author__ = 'David'

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')


def proof_of_concept(arg):
    # os.system("gnome-terminal -e 'bash -c \"echo %s; exec bash\"'" % arg)
    os.system("start cmd /k echo %s" % arg)
    return arg


def on_request(ch, method, props, body):
    n = str(body)
    print("Starting terminal printing %s" % (n,))
    response = proof_of_concept(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()
