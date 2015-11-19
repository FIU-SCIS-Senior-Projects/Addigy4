import pika
__author__ = 'David'


class PubSub(object):
    # Constructor for the pubsub instance. Connects to a specified RabbitMQ server and sets aside a queue on said server
    # called whatever the user specifies ('' by default)
    def __init__(self, addr=None, port=None, virtual_host=None, queue_name=None, username=None,
                 password=None, channel_max=None,
                 frame_max=None, heartbeat_interval=None,
                 ssl=None, ssl_options=None, connection_attempts=None, retry_delay=None, socket_timeout=None,
                 locale=None,
                 backpressure_detection=None, passive=False, exclusive=False, auto_delete=False, arguments=None,
                 organization=''):

        self.username = username
        self.password = password
        self.MESSAGES_EXCHANGE = organization+".messages"
        self.PRESENCE_EXCHANGE = organization+".presence"

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

    def create_queue(self, queue_name=None, passive=None, auto_delete=False, exclusive=None, arguments=None):
        self.channel.queue_declare(queue=queue_name, passive=passive, auto_delete=auto_delete,
                                   exclusive=exclusive, arguments=arguments)
    
    def publish(self, routing_key, body, properties=None, mandatory=False, immediate=False, persistance=False):
        if persistance is False:
            self.channel.basic_publish(exchange=self.MESSAGES_EXCHANGE, routing_key=routing_key, body=body, properties=properties,
                                       mandatory=mandatory, immediate=immediate)
        else:
            self.channel.basic_publish(exchange=self.MESSAGES_EXCHANGE, routing_key=routing_key, body=body, properties=pika.BasicProperties(delivery_mode=2,),
                                       mandatory=mandatory, immediate=immediate)

    def subscribe(self, callback, queue_name, no_ack=False, exclusive=False, consumer_tag=None, arguments=None):
        self.channel.queue_bind(exchange=self.PRESENCE_EXCHANGE, routing_key=self.username, queue=queue_name)
        self.channel.queue_bind(queue=queue_name, exchange=self.PRESENCE_EXCHANGE, routing_key='')
        self.channel.queue_bind(exchange=self.MESSAGES_EXCHANGE,
                                queue=queue_name)
        self.channel.basic_consume(callback, queue=queue_name, no_ack=no_ack, exclusive=exclusive, consumer_tag=consumer_tag,
                                   arguments=arguments)

        self.channel.start_consuming()

    def acknowledge(self, delivery_tag=None):
        self.channel.basic_ack(delivery_tag=delivery_tag)

    def get_messageexchange(self):
        return self.MESSAGES_EXCHANGE

    def get_presenceexchange(self):
        return self.PRESENCE_EXCHANGE

    def disconnect(self):
        self.connection.close()
