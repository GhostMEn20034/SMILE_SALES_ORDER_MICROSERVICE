from django.db.models import QuerySet

from apps.refunds.models import Refund
from param_classes.refunds.refund_request_creation import RefundRequestCreationParams


class RefundService:
    def __init__(self, refund_queryset: QuerySet[Refund]):
        self.refund_queryset = refund_queryset

    def create_refund(self, params: RefundRequestCreationParams) -> Refund:
        refund: Refund = self.refund_queryset.create(
            reason_for_return=params.reason_for_return,
            user_id=params.user_id,
            order_id=params.order_id,
        )
        return refund

    @staticmethod
    def approve_refund(refund: Refund) -> Refund:
        refund.approve()
        return refund

    @staticmethod
    def reject_refund(refund: Refund, reject_reason: str) -> Refund:
        refund.reject(reject_reason)
        return refund
