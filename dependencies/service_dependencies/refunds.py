from apps.refunds.models import Refund
from services.refunds.refund_service import RefundService


def get_refund_service() -> RefundService:
    refund_queryset = Refund.objects.all()
    return RefundService(refund_queryset, )
