import logging
from typing import Optional
from django.db import transaction

from apps.accounts.serializers.replication import AccountReplicationSerializer
from services.carts.replication.create import CartCreator

class AccountCreator:
    """
    Responsible for creating accounts with the data sent by the other server via message broker.
    """
    @staticmethod
    def create_one(data: dict) -> Optional[dict]:
        user = data.get('user')
        cart = data.get('cart')
        cart_items = data.get('cart_items')

        response = {}

        with transaction.atomic():
            serializer = AccountReplicationSerializer(data=user)
            if not serializer.is_valid():
                logging.error(serializer.errors)
                logging.info("Unable to serialize data and create a User")
                return None
            else:
                serializer.save()
                response["user"] = serializer.data

                if cart:
                    cart_data = CartCreator.create_cart(cart)
                    response["cart"] = cart_data

                if cart_items:
                    cart_items_data = CartCreator.create_many_cart_items(cart_items)
                    response["cart_items"] = cart_items_data

        return response
