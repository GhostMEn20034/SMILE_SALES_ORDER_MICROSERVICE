from decimal import Decimal
from typing import List

from services.payments.payment_params.paypal.purchase_unit_params import PurchaseItem


class PurchaseUnitBuildResult:
    def __init__(self, purchase_unit_items: List[PurchaseItem], total_items_amount: Decimal, total_items_tax: Decimal):
        self.purchase_unit_items = purchase_unit_items # All items the user wants to purchase
        self.total_items_amount = total_items_amount # Total amount for the all items (Without taxes)
        self.total_items_tax = total_items_tax # Total tax for the all items