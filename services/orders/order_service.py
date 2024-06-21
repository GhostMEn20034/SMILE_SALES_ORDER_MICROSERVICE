from django.db.models import QuerySet

from apps.orders.models import Order
from services.payments.payment_service import PaymentService


class OrderService:
    def __init__(self, order_queryset: QuerySet[Order], payment_service: PaymentService):
        self.order_queryset = order_queryset
        self.payment_service = payment_service

    def create_order(self):
        payment_data = self.payment_service.create_paypal_payment()
        return payment_data
