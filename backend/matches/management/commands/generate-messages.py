from django.core.management.base import BaseCommand, CommandError
import pika
import datetime
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        parameters = pika.URLParameters(
            f'amqp://guest:guest@{settings.AMQP_HOST}:{settings.AMQP_PORT}/%2F')
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        for x in range(10000):
            channel.basic_publish('test_exchange',
                    'test_routing_key',
                    str(datetime.datetime.utcnow()),
                    pika.BasicProperties(content_type='text/plain',
                        delivery_mode=1))
        connection.close()
