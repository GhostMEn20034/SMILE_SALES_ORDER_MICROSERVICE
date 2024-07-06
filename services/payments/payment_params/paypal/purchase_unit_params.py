from typing import List

from services.payments.payment_params.paypal.amount_params import UnitAmount, AmountBreakdown, TaxAmount
from services.payments.payment_params.paypal.base.amount import AmountParamBase


class AmountParam(AmountParamBase):
    """
    The total order amount.
    PROPERTIES:
        value: The value, which might be:
            - An integer for currencies like JPY that are not typically fractional.
            - A decimal fraction for currencies like TND that are subdivided into thousandths.
        currency_code: The three-character ISO-4217 currency code that identifies the currency.
    """

    def __init__(self, value: str, currency_code: str, amount_breakdown: AmountBreakdown):
        super().__init__(value, currency_code, )
        self.breakdown = amount_breakdown

    def to_dict(self):
        return {
            'value': self.value,
            'currency_code': self.currency_code,
            'breakdown': self.breakdown.to_dict(),
        }


class PurchaseItem:
    """
    An item that the customer purchases from the merchant.
    PROPERTIES:
        name: The name of the item.
        quantity: The item quantity.
        url: The URL to the item being purchased. Visible to buyer and used in buyer experiences.
        sku: The stock keeping unit (SKU) for the item.
        image_url: The URL of the item's image.
        unit_amount: The item price or rate per unit.
    """
    def __init__(self, name: str, quantity: int, url: str, sku: str,
                 image_url: str, unit_amount: UnitAmount, tax: TaxAmount):
        self.name = name
        self.quantity = quantity
        self.url = url
        self.sku = sku
        self.image_url = image_url
        self.unit_amount = unit_amount
        self.tax = tax

    def to_dict(self):
        return {
            'name': self.name,
            'quantity': self.quantity,
            'url': self.url,
            'sku': self.sku,
            'image_url': self.image_url,
            'unit_amount': self.unit_amount.to_dict(),
            'tax': self.tax.to_dict(),
        }


class PurchaseUnit:
    """
    Each purchase unit establishes a contract between a payer and the payee.
    Each purchase unit represents either a full
    or partial order that the payer intends to purchase from the payee.

    PROPERTIES:
        reference_id: The API caller-provided external ID for the purchase unit.
                      Required for multiple purchase units when you must update the order through PATCH.
        description: The purchase description.
        amount: The total order amount.
        items: An array of items that the customer purchases from the merchant.

    """
    def __init__(self, reference_id: str, description: str, amount: AmountParam, items: List[PurchaseItem]):
        self.reference_id = reference_id
        self.description = description
        self.amount = amount
        self.items = items

    def to_dict(self):
        return {
            "reference_id": self.reference_id,
            "description": self.description,
            "amount": self.amount.to_dict(),
            "items": [item.to_dict() for item in self.items],
        }
