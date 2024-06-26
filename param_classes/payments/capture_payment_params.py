import uuid


class CapturePaymentParams:
    def __init__(self, order_id: uuid.UUID, payment_id: str):
        self.order_id = order_id
        self.payment_id = payment_id
