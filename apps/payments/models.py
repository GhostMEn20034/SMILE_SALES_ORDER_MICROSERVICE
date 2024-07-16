from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F

from .choices import PaymentStatuses, PaymentTypes
from apps.orders.models import Order


User = get_user_model()


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field="original_id")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, to_field="order_uuid", related_name="payments")
    net_amount = models.DecimalField(max_digits=15, decimal_places=2)
    provider_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    gross_amount = models.GeneratedField(
        expression=F('net_amount') + F('provider_fee'),
        output_field=models.DecimalField(max_digits=16, decimal_places=2),
        db_persist=True
    )
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=15, choices=PaymentStatuses.choices, default=PaymentStatuses.PENDING)
    provider = models.CharField(max_length=30)
    type = models.CharField(max_length=15, choices=PaymentTypes.choices, default=PaymentTypes.PAYMENT)
    provider_payment_id = models.CharField(max_length=255, unique=True) # Payment identifier given
    # by the payment provider
    capture_id = models.CharField(max_length=255, blank=True, null=True) # Optional field for capture ID if applicable
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.provider} payment {self.provider_payment_id}"
