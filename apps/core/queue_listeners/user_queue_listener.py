from django.conf import settings

from .base_queue_listener import BaseQueueListener
from message_handlers.user_queue_handler import handle_user_queue


class UserQueueListener(BaseQueueListener):
    BINDING_KEY = 'users.#'
    exchange_name = settings.USERS_DATA_CRUD_EXCHANGE_TOPIC_NAME
    message_handler_func = staticmethod(handle_user_queue)
