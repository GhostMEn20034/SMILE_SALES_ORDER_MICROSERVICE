import uuid

from services.payments.payment_params.base.capture import Capture


class PaymentCreationParams:
    def __init__(self, payment_id: str, capture: Capture, user_id: int, order_id: uuid.UUID,
                 provider: str, status: str):
        self.payment_id = payment_id
        self.capture = capture
        self.user_id = user_id
        self.order_id = order_id
        self.provider = provider
        self.status = status
