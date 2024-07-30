from typing import Optional

from apps.orders.models import Order
from apps.payments.models import Payment


class OrderCancellationResult:
    def __init__(self, order: Order, payment: Optional[Payment] = None):
        self.order = order
        self.payment = payment
