import pika

__author__ = 'David'


class PubSub(object):
    # Constructor for the pubsub instance. Connects to a specified RabbitMQ server and sets aside a queue on said server
    # called whatever the user specifies ('' by default)
    def __init___(self, callback, addr=None, port=None, virtual_host=None, queue_name=None, credentials=None,
                  channel_max=None,
                  frame_max=None, heartbeat_interval=None,
                  ssl=None, ssl_options=None, connection_attempts=None, retry_delay=None, socket_timeout=None,
                  locale=None,
                  backpressure_detection=None, passive=False, exclusive=False, auto_delete=False, arguments=None):

        global channel
        global connection

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(addr=addr, port=port, virtual_host=virtual_host, credentials=credentials,
                                      channel_max=channel_max, frame_max=frame_max,
                                      heartbeat_interval=heartbeat_interval, ssl=ssl, ssl_options=ssl_options,
                                      connection_attempts=connection_attempts, retry_delay=retry_delay,
                                      socket_timeout, locale, backpressure_detection=backpressure_detection))

        channel = connection.channel()

        # If we send the message to a non-existant location, RabbitMQ will trash the message.
        # Here we declare a queue to which the message will get sent to in the broker
        channel.queue_declare(queue=queue_name, passive=passive, callback, auto_delete=auto_delete,
                          exclusive=exclusive, arguments=arguments)

    def publish(self, exchange, routing_key, body, properties=None, mandatory=False, immediate=False):

        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body, properties=properties,
                              mandatory=mandatory, immediate=immediate)

    def subscribe(self, callback, queue_name, no_ack=False, exclusive=False, consumer_tag=None, arguments=None):
        channel.basic_consume(callback, queue=queue_name, no_ack=no_ack, exclusive=exclusive, consumer_tag=consumer_tag,
                              arguments=arguments)

        channel.start_consuming()
