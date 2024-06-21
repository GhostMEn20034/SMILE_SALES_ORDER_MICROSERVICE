from typing import Union, List
from django.db.models import QuerySet

from apps.products.models import Product


class BuildPurchaseUnitParams:
    def __init__(self, reference_id: str, description: str,
                          products: Union[List[Product], QuerySet[Product]], currency_code: str):
        self.reference_id = reference_id
        self.description = description
        self.products = products
        self.currency_code = currency_code