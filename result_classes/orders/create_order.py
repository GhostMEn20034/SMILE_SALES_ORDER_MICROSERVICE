from typing import List, Union

from django.db.models import QuerySet

from apps.orders.models import Order, OrderItem


class CreateOrderResult:
    def __init__(self, order: Order,
                 order_items: Union[List[OrderItem], QuerySet[OrderItem]]):
        self.order = order
        self.order_items = order_items
