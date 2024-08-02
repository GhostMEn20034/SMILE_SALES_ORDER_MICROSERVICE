from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .choices import RefundStatus, ReturnReason
from apps.orders.models import Order


Account = get_user_model()


class Refund(models.Model):
    reason_for_return = models.CharField(max_length=50, choices=ReturnReason.choices)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, to_field="order_uuid")
    user = models.ForeignKey(Account, on_delete=models.CASCADE, to_field='original_id')
    status = models.CharField(max_length=10, choices=RefundStatus.choices, default=RefundStatus.PENDING)
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)

    def approve(self):
        self.status = RefundStatus.APPROVED
        self.approval_date = timezone.now()
        self.save()

    def reject(self, reason):
        self.status = RefundStatus.REJECTED
        self.rejection_date = timezone.now()
        self.rejection_reason = reason
        self.save()

    def __str__(self):
        return f"RefundRequest for Order {self.order_id} - {self.status}"

    class Meta:
        verbose_name = "Refund Request"
        verbose_name_plural = "Refund Requests"