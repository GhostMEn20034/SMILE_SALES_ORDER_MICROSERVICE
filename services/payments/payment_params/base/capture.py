from typing import Optional

from services.payments.payment_params.paypal.base.amount import AmountParamBase


class Capture:
    def __init__(self, gross_amount: AmountParamBase, provider_fee: AmountParamBase,
                 net_amount: AmountParamBase, capture_id: Optional[str] = None, ):
        self.capture_id = capture_id
        self.gross_amount = gross_amount
        self.provider_fee = provider_fee
        self.net_amount = net_amount
