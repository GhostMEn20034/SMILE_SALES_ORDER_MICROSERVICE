from typing import Literal, List

from .purchase_unit_params import PurchaseUnit
from .payment_source import PayPalPaymentSource


class CreatePaypalPaymentParams:
    """
        Represents data essential for creating a PayPal payment.
        PROPERTIES:
            intent: The intent to either capture payment immediately
                    or authorize a payment for an order after order creation.
            purchase_unit: An array of purchase units.
                           Each purchase unit establishes a contract between a payer and the payee.
            paypal_payment_source: Indicates that PayPal Wallet is the payment source.
                                   Main use of this selection is
                                   to provide additional instructions associated with this choice like vaulting.
    """
    def __init__(self, intent: Literal["CAPTURE", "AUTHORIZE"],
                 purchase_units: List[PurchaseUnit], paypal_payment_source: PayPalPaymentSource):
        self.intent = intent
        self.purchase_units = purchase_units
        self.paypal_payment_source = paypal_payment_source
