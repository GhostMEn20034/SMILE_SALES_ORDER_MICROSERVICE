from uuid import UUID

from apps.payments.models import Payment
from apps.refunds.models import Refund


class RefundPaymentApprovalParams:
    def __init__(self, payment: Payment, refund_reason: str, order_id: UUID, user_id: int):
        self.user_id = user_id
        self.order_id = order_id
        self.refund_reason = refund_reason
        self.payment = payment
