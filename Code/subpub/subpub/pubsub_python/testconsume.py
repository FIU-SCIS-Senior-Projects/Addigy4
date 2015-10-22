import pubsub
__author__ = 'David'

sample = pubsub.PubSub(addr='localhost', queue_name='hello')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))

sample.subscribe(callback, queue_name='hello', no_ack=True)
