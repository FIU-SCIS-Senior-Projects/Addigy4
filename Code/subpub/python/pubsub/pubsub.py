import time
import pika
import requests
__author__ = 'David'


class PubSub(object):
    # Constructor for the pubsub instance. Connects to a specified RabbitMQ server and sets aside a queue on said server
    # called whatever the user specifies ('' by default)
    def __init__(self, addr=None, port=None, virtual_host=None, queue_name=None, username=None,
                 password=None, channel_max=None,
                 frame_max=None, heartbeat_interval=None,
                 ssl=None, ssl_options=None, connection_attempts=None, retry_delay=None, socket_timeout=None,
                 locale=None,
                 backpressure_detection=None, passive=False, exclusive=False, auto_delete=False, arguments=None):

        self.username = username
        self.password = password
        self.MESSAGES_EXCHANGE = "messages"
        self.PRESENCE_EXCHANGE = "presence"
        self.CURRENT_TIME = int(round(time.time() * 1000))

        credentials = pika.PlainCredentials(self.username, self.password)

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=addr, port=port, virtual_host=virtual_host, credentials=credentials,
                                      channel_max=channel_max, frame_max=frame_max,
                                      heartbeat_interval=heartbeat_interval, ssl=ssl, ssl_options=ssl_options,
                                      connection_attempts=connection_attempts, retry_delay=retry_delay,
                                      backpressure_detection=backpressure_detection))

        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.PRESENCE_EXCHANGE,
                                      exchange_type='x-presence',
                                      auto_delete=auto_delete)

        self.channel.exchange_declare(exchange=self.MESSAGES_EXCHANGE,
                                      exchange_type='fanout',
                                      auto_delete=auto_delete)

        # If we send the message to a non-existant location, RabbitMQ will trash the message.
        # Here we declare a queue to which the message will get sent to in the broker
        if queue_name is not None:
            self.channel.queue_declare(queue=queue_name, passive=passive, auto_delete=auto_delete,
                                       exclusive=exclusive, arguments=arguments)

    def create_queue(queue_name=None, passive=None, auto_delete=False, exclusive=None, arguments=None):
        self.channel.queue_declare(queue=queue_name, passive=passive, auto_delete=auto_delete,
                                   exclusive=exclusive, arguments=arguments)
    
    def publish(self, routing_key, body, properties=None, mandatory=False, immediate=False):
        self.channel.basic_publish(exchange=self.MESSAGES_EXCHANGE, routing_key=routing_key, body=body, properties=properties,
                                   mandatory=mandatory, immediate=immediate)

    def subscribe(self, callback, queue_name, no_ack=False, exclusive=False, consumer_tag=None, arguments=None):
        self.channel.queue_bind(exchange=self.PRESENCE_EXCHANGE, routing_key=self.username, queue=queue_name)
        self.channel.queue_bind(queue=queue_name, exchange=self.PRESENCE_EXCHANGE, routing_key='')
        self.channel.queue_bind(exchange=self.MESSAGES_EXCHANGE,
                                queue=queue_name)
        self.channel.basic_consume(callback, queue=queue_name, no_ack=no_ack, exclusive=exclusive, consumer_tag=consumer_tag,
                                   arguments=arguments)

        self.channel.start_consuming()

    def get_messageexchange(self):
        return self.MESSAGES_EXCHANGE

    def get_presenceexchange(self):
        return self.PRESENCE_EXCHANGE

    def disconnect(self):
        self.connection.close()

    def idle_limit(self):
        JSON = requests.get('http://localhost:15672/api/channels', auth=('guest', 'guest')).json()
        idle_since = self.find_between(" ", ",\"tr")
        return idle_since

    def find_between(self, original_string, first, last):
        try:
            start = original_string.index(first) + len(first)
            end = original_string.index(last, start)
            return original_string[start:end]
        except ValueError:
            return ""
