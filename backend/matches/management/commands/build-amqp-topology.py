import pika
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        parameters = pika.URLParameters(
            f'amqp://guest:guest@{settings.AMQP_HOST}:{settings.AMQP_PORT}/%2F')
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
