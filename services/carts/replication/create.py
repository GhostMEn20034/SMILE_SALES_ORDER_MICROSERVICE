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
        serializer = CartItemReplicationSerializer(data=data, many=True)
        if serializer.is_valid():
            created_cart_items = CartItem.objects.bulk_create(serializer.data)
            return CartItemReplicationSerializer(created_cart_items, many=True).data
        else:
            logging.error(serializer.errors)
            logging.info("Unable to serialize data and create a Cart Items")
