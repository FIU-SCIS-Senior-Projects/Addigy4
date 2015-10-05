import pubsub_python
__author__ = 'David'

sample = pubsub_python.PubSub(host='localhost', queue_name='hello')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))

sample.consume(callback, queue_name='hi', no_ack=True)
