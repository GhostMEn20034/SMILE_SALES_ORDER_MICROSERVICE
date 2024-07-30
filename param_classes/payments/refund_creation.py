import uuid

from services.payments.payment_params.paypal.refund_breakdown import RefundBreakdown


class RefundCreationParams:
    def __init__(self, refund_id: str, user_id: int, order_id: uuid.UUID,
                 provider: str, status: str, refund_breakdown: RefundBreakdown,):
        self.refund_id = refund_id
        self.user_id = user_id
        self.order_id = order_id
        self.provider = provider
        self.status = status
        self.refund_breakdown = refund_breakdown
