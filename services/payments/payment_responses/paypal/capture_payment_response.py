from typing import List

from services.payments.payment_params.base.capture import Capture


class CapturePayPalPaymentResponse:
    def __init__(self, payment_id: str, captures: List[Capture]):
        self.payment_id = payment_id
        self.captures = captures
