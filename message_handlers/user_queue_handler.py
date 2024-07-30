from typing import Any

from services.accounts.account_queue_message_handler import handle_account_queue_message
from services.addresses.address_queue_message_handler import handle_address_queue_message
from services.carts.cart_queue_message_handler import handle_cart_queue_message

def handle_user_queue(routing_key: str, message: Any):
    if routing_key.startswith("users.accounts"):
        handle_account_queue_message(routing_key, message)
    elif routing_key.startswith("users.addresses"):
        handle_address_queue_message(routing_key, message)
    elif routing_key.startswith("users.carts") or routing_key.startswith("users.cart_items"):
        handle_cart_queue_message(routing_key, message)
