import uuid

from apps.refunds.models import Refund


class RefundTestingUtils:

    @staticmethod
    def create_refund(user_id: int, order_id: uuid.UUID, reason_for_return: str) -> Refund:
        refund = Refund.objects.create(
            order_id=order_id,
            user_id=user_id,
            reason_for_return=reason_for_return,
        )

        return refund