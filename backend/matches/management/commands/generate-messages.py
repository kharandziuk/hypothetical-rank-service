from django.core.management.base import BaseCommand, CommandError
import pika
import datetime
from django.conf import settings
import itertools
from time import sleep

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_messages():
    result = []
    for x in range(1, 5):
        path = settings.BASE_DIR / "artifacts" / f"message{x}.json"
        with open(path) as msg_file:
            result.append(msg_file.read())
    return result


class Command(BaseCommand):
    def handle(self, *args, **options):
        c_string = f"amqp://guest:guest@{settings.AMQP_HOST}:{settings.AMQP_PORT}/%2F"
        parameters = pika.URLParameters(c_string)
        connection = pika.BlockingConnection(parameters)
        messages = get_messages()
        channel = connection.channel()
        try:
            for msg in itertools.cycle(messages):
                logger.debug(".")
                channel.basic_publish(
                    "test_exchange",
                    "test_routing_key",
                    msg,
                    pika.BasicProperties(content_type="text/plain", delivery_mode=1),
                )
                sleep(0.03)
        except KeyboardInterrupt:
            connection.close()
