import pubsub
__author__ = 'David'

sample = pubsub.PubSub(addr='localhost', queue_name='guest', username='guest', password='guest', auto_delete=True)

print("Listening on hello")

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

try:
    sample.subscribe(callback, queue_name='guest', no_ack=True)
except KeyboardInterrupt:
    sample.disconnect()
