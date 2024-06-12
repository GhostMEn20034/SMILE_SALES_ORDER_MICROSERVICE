import logging
from typing import List

from apps.carts.serializers.replication import CartReplicationSerializer, CartItemReplicationSerializer
from apps.carts.models import CartItem


class CartCreator:
    """
    Responsible for creating carts / cart items with the data sent by the other server via message broker.
    """
    @staticmethod
    def create_cart(data: dict) -> dict:
        serializer = CartReplicationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return serializer.validated_data
        else:
            logging.error(serializer.errors)
            logging.info("Unable to serialize data and create a Cart")

    @staticmethod
    def create_one_cart_item(data: dict) -> dict:
        serializer = CartItemReplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.validated_data
        else:
            logging.error(serializer.errors)
            logging.info("Unable to serialize data and create a Cart Item")

    @staticmethod
    def create_many_cart_items(data: List[dict]) -> List[dict]:
        cart_items = []
        for cart_item in data:
            serializer = CartItemReplicationSerializer(data=cart_item)
            if not serializer.is_valid():
                logging.error(serializer.errors)
                raise ValueError("Unable to deserialize data and create a Cart Item")
            else:
                cart_items.append(CartItem(**serializer.validated_data))

        CartItem.objects.bulk_create(cart_items)
        return data