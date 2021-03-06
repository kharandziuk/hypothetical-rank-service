import pika
import json
from django.core.management.base import BaseCommand, CommandError

from matches import models
from django.conf import settings

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def on_message(channel, method_frame, header_frame, body):
    logger.debug("handle message")
    msg = json.loads(body.decode("utf-8"))
    models.Match.objects.from_msg(msg)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


class Command(BaseCommand):
    def handle(self, *args, **options):
        c_string = f"amqp://guest:guest@{settings.AMQP_HOST}:{settings.AMQP_PORT}/%2F"
        logger.debug(c_string)
        parameters = pika.URLParameters(c_string)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        # TODO: hardcoded value
        channel.basic_consume("test", on_message)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        connection.close()
