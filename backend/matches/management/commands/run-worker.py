import pika
from django.core.management.base import BaseCommand, CommandError

from matches import models
from django.conf import settings



def on_message(channel, method_frame, header_frame, body):
    models.Match.objects.create(name=body)

class Command(BaseCommand):
    def handle(self, *args, **options):
        c_string = f'amqp://guest:guest@{settings.AMQP_HOST}:{settings.AMQP_PORT}/%2F'
        self.stdout.write(c_string)
        parameters = pika.URLParameters(
            c_string
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.basic_consume('test', on_message)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        connection.close()

