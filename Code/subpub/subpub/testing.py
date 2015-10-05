import pubsub_python
__author__ = 'David'

sample = pubsub_python.PubSub(host='localhost', queue_name='hello')

sample.publish(exchange='', routing_key='hello', body='Test')
