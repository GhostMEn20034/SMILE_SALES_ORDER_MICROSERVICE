from django.conf import settings

from .base_queue_listener import BaseQueueListener
from message_handlers.product_queue_message_handler import handle_product_queue_message

class ProductQueueListener(BaseQueueListener):
    BINDING_KEY = 'products.#'
    exchange_name = settings.PRODUCT_CRUD_EXCHANGE_TOPIC_NAME
    message_handler_func = staticmethod(handle_product_queue_message)
