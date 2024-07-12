from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Order

@receiver(pre_save, sender=Order)
def update_order_dates(sender, instance,  **kwargs):
    if instance.pk:  # Check if this is an update, not a new creation
        previous_order = Order.objects.get(pk=instance.pk)
        if previous_order.status != instance.status:
            if instance.status == 'shipped' and not instance.shipped_at:
                instance.shipped_at = timezone.now()
            if instance.status == 'cancelled' and not instance.cancelled_at:
                instance.cancelled_at = timezone.now()
            if instance.status == 'delivered' and not instance.delivered_at:
                instance.delivered_at = timezone.now()
