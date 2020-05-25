import pika
from django.core.management.base import BaseCommand, CommandError

from matches import models



def on_message(channel, method_frame, header_frame, body):
    models.Match.objects.create(name=body)

class Command(BaseCommand):
    def handle(self, *args, **options):
        connection = pika.BlockingConnection()
        channel = connection.channel()
        channel.basic_consume('test', on_message)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        connection.close()

