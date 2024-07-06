from typing import Union, List
from django.db.models import QuerySet

from apps.orders.models import OrderItem


class BuildPurchaseUnitParams:
    def __init__(self, reference_id: str, description: str,
                          order_items: Union[List[OrderItem], QuerySet[OrderItem]], currency_code: str):
        self.reference_id = reference_id
        self.description = description
        self.order_items = order_items
        self.currency_code = currency_code