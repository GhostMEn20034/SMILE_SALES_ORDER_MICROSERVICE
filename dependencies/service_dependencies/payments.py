from services.payments.payment_service import PaymentService


def get_payment_service() -> PaymentService:
    return PaymentService()