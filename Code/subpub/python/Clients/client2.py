#!/usr/bin/env python
import pubsub
import threading
__author__ = 'David'

sample = pubsub.PubSub(addr='localhost', queue_name='guest', username='guest', password='guest', auto_delete=True,
                       heartbeat_interval=2)

MESSAGES_EXCHANGE = sample.get_messageexchange()
PRESENCE_EXCHANGE = sample.get_presenceexchange()


def callback(channel, method_frame, header_frame, body):
        exchange = method_frame.exchange
        if exchange == PRESENCE_EXCHANGE:
            action = header_frame.headers['action']
            who = header_frame.headers['key']
            if action == 'bind':
                print('User %s entered the room.' % (who,))
            elif action == 'unbind':
                print('User %s left the room.' % (who,))
        elif exchange == MESSAGES_EXCHANGE:
            who = method_frame.routing_key
            print('%s: %s' % (who, body))

started = False


def consume():
        sample.subscribe(callback, queue_name='guest', no_ack=True)


while True:
    if started is False:
        thread = threading.Thread(target=consume)
        thread.start()
        started = True

    message = input("\n")

    if message == "exit":
        sample.disconnect()

    sample.publish(routing_key='guest',
                   body=message)


