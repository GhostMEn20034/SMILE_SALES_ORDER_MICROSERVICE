from django.db.models import QuerySet

from apps.orders.models import Order
from apps.payments.models import Payment


class OrderDetailsResult:
    def __init__(self, order: Order, payments: QuerySet[Payment]):
        self.order = order
        self.payments = payments