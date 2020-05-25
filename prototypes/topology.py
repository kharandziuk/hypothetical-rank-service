import pika
parameters = pika.URLParameters(
    f'amqp://guest:guest@localhost:5672/%2F')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
queue = channel.queue_declare(queue='test')
channel.exchange_declare(
    exchange='test_exchange',
    exchange_type='fanout'
)

channel.queue_bind(
    exchange='test_exchange',
    queue=queue.method.queue
)
