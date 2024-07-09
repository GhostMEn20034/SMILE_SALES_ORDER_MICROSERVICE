import uuid


class CapturePaymentParams:
    def __init__(self, order_id: uuid.UUID, payment_id: str, user_id: int, provider: str):
        self.order_id = order_id
        self.payment_id = payment_id
        self.user_id = user_id
        self.provider = provider # payment provider
