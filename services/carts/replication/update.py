import logging
from typing import Optional

from apps.carts.models import CartItem
from apps.carts.serializers.replication import CartItemReplicationSerializer


class CartModifier:
    """
    Responsible for updating carts / cart items with the data sent by the other server via message broker.
    """
    @staticmethod
    def update_one_cart_item(data: dict) -> Optional[dict]:
        try:
            cart_item = CartItem.objects.get(original_id=data.pop("original_id"))
        except CartItem.DoesNotExist:
            logging.error("Cannot find a cart item to update")
            return None

        data = CartItemReplicationSerializer(instance=cart_item, data=data, partial=True)
        if data.is_valid():
            data.save()
            return data.data
        else:
            logging.error(data.errors)