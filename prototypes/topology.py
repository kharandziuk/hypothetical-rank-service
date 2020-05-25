import pika
connection = pika.BlockingConnection()
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
