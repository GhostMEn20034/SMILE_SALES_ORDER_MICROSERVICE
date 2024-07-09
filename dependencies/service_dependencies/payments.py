from apps.payments.models import Payment
from services.payments.payment_service import PaymentService


def get_payment_service() -> PaymentService:
    payment_queryset = Payment.objects.all()
    return PaymentService(payment_queryset)