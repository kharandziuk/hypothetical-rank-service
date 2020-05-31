from django.core.management.base import BaseCommand, CommandError
import pika
import datetime
from django.conf import settings
import itertools


class Command(BaseCommand):
    def handle(self, *args, **options):
        c_string = f'amqp://guest:guest@{settings.AMQP_HOST}:{settings.AMQP_PORT}/%2F'
        print(c_string)
        parameters = pika.URLParameters(c_string)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        for x in itertools.count():
            channel.basic_publish('test_exchange',
                    'test_routing_key',
                    str(datetime.datetime.utcnow()),
                    pika.BasicProperties(content_type='text/plain',
                        delivery_mode=1))
        connection.close()
