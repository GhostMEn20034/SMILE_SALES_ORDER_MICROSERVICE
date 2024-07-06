from typing import List, Union
from django.db.models import QuerySet

from apps.carts.models import CartItem


class CreateOrderParams:
    """
    Params essential to insert order and order items into the DB.
    """
    def __init__(self, user_id: int, address_id: int, product_ids: List[str],
                 cart_items: Union[List[CartItem], QuerySet[CartItem]]):
        self.user_id = user_id
        self.address_id = address_id
        self.product_ids = product_ids
        self.cart_items = cart_items
