from django.db.models import TextChoices

class PaymentStatuses(TextChoices):
    PENDING = 'pending', "Pending"
    SUCCESS = 'success', "Successful"
    CANCELED = 'canceled', "Canceled"
    FAILED = 'failed', "Failed"


class PaymentTypes(TextChoices):
    PAYMENT = 'payment', "Payment"
    REFUND = 'refund', "Refund"
