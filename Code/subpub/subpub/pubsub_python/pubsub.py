import pika

__author__ = 'David'


class PubSub(object):
    # Constructor for the pubsub instance. Connects to a specified RabbitMQ server and sets aside a queue on said server
    # called whatever the user specifies ('' by default)
    def __init__(self, username=None, addr=None, port=None, virtual_host=None, queue_name=None, credentials=None,
                  channel_max=None,
                  frame_max=None, heartbeat_interval=None,
                  ssl=None, ssl_options=None, connection_attempts=None, retry_delay=None, socket_timeout=None,
                  locale=None,
                  backpressure_detection=None, passive=False, exclusive=False, auto_delete=False, arguments=None):

        self.MESSAGES_EXCHANGE = queue_name + "messages"
        self.PRESENCE_EXCHANGE = queue_name + "presence"

        self.username = username
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=addr, port=port, virtual_host=virtual_host, credentials=credentials,
                                      channel_max=channel_max, frame_max=frame_max,
                                      heartbeat_interval=heartbeat_interval, ssl=ssl, ssl_options=ssl_options,
                                      connection_attempts=connection_attempts, retry_delay=retry_delay,
                                      backpressure_detection=backpressure_detection))

        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.PRESENCE_EXCHANGE,
                                      exchange_type='x-presence')

        self.channel.exchange_declare(exchange=self.MESSAGES_EXCHANGE,
                                      exchange_type='fanout')

        # If we send the message to a non-existant location, RabbitMQ will trash the message.
        # Here we declare a queue to which the message will get sent to in the broker
        self.channel.queue_declare(queue=queue_name, passive=passive, auto_delete=auto_delete,
                          exclusive=exclusive, arguments=arguments)

    def publish(self, routing_key, body, properties=None, mandatory=False, immediate=False):
        self.channel.basic_publish(exchange=self.MESSAGES_EXCHANGE, routing_key=routing_key, body=body, properties=properties,
                              mandatory=mandatory, immediate=immediate)

    def subscribe(self, callback, queue_name, no_ack=False, exclusive=False, consumer_tag=None, arguments=None):
        self.channel.basic_consume(callback, queue=queue_name, no_ack=no_ack, exclusive=exclusive, consumer_tag=consumer_tag,
                              arguments=arguments)

        self.channel.start_consuming()

    def on_queue_declare(self, reply):
        self.private_queue = reply.method.queue
        self.channel.queue_bind(None, self.private_queue, self.PRESENCE_EXCHANGE, self.username)
        self.channel.queue_bind(None, self.private_queue, self.PRESENCE_EXCHANGE, '')
        self.channel.queue_bind(None, self.private_queue, self.MESSAGES_EXCHANGE)
        self.channel.basic_consume(self.on_message, self.private_queue)

    def on_message(self, channel, method_frame, header_frame, body):
        self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        exchange = method_frame.exchange
        if exchange == self.PRESENCE_EXCHANGE:
            action = header_frame.headers['action']
            who = header_frame.headers['key']
            if action == 'bind':
                print('User %s entered the room.') % (who,)
            elif action == 'unbind':
                print('User %s left the room.' % (who,))
        elif exchange == self.MESSAGES_EXCHANGE:
            who = method_frame.routing_key
            print('%s: %s' % (who, body))