import json
import threading
import logging
from django.conf import settings

from ..message_broker.base.consumer import Consumer
from services.accounts.account_queue_message_handler import handle_account_queue_message
from services.addresses.address_queue_message_handler import handle_address_queue_message
from services.carts.cart_queue_message_handler import handle_cart_queue_message


BINDING_KEY = 'users.#'


class UserQueueListener(threading.Thread):
    def __init__(self):
        super().__init__()
        self.consumer = Consumer(
            exchange_name=settings.USERS_DATA_CRUD_EXCHANGE_TOPIC_NAME,
            exchange_type="topic"
        )
        self.consumer.bind_queue(BINDING_KEY)

    def callback(self, ch, method, properties, body):
        routing_key: str = method.routing_key
        print(f" [x] {routing_key}:{json.loads(body)}")

        if routing_key.startswith("users.accounts"):
            handle_account_queue_message(routing_key, json.loads(body))
        elif routing_key.startswith("users.addresses"):
            handle_address_queue_message(routing_key, json.loads(body))
        elif routing_key.startswith("users.carts") or routing_key.startswith("users.cart_items"):
            handle_cart_queue_message(routing_key, json.loads(body))

    def run(self):
        logging.info('Users Data Queue Listener was launched')
        self.consumer.consume(callback=self.callback)
