import pika
__author__ = 'David'


# Constructor for the pubsub instance. Connects to a specified RabbitMQ server
def __init___(self, addr, port, virtual_host, queue_name, credentials, channel_max, frame_max, heartbeat_interval,
              ssl, ssl_options, connection_attempts, retry_delay, socket_timeout, locale, backpressure_detection):
    connection = pika.BlockingConnection(pika.ConnectionParameters(addr))

    channel = connection.channel()

    # If we send the message to a non-existant location, RabbitMQ will trash the message.
    # Here we declare a queue to which the message will get sent to in the broker
    channel.queue_declare(queue=queue_name)

