from typing import Any

from .replication.create import CartCreator
from .replication.update import CartModifier
from .replication.delete import CartRemover


def handle_cart_queue_message(routing_key: str, message: Any):
    if routing_key == 'users.carts.create.one':
        return CartCreator.create_cart(message)
    elif routing_key == 'users.carts.clear':
        return CartRemover.clear_cart(message)
    elif routing_key == 'users.carts.delete_inactive_carts':
        return CartRemover.delete_inactive_carts(message)
    elif routing_key == 'users.cart_items.create.one':
        return CartCreator.create_one_cart_item(message)
    elif routing_key == 'users.cart_items.create.many':
        return CartCreator.create_many_cart_items(message)
    elif routing_key == 'users.cart_items.update.one':
        return CartModifier.update_one_cart_item(message)
    elif routing_key == 'users.cart_items.delete.one':
        return CartRemover.remove_one_cart_item(message)
