from django.db import models

class RefundStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'

class ReturnReason(models.TextChoices):
    DAMAGED = 'damaged', 'Damaged'
    NOT_AS_DESCRIBED = 'not_as_described', 'Not as Described'
    WRONG_ITEM = 'wrong_item', 'Wrong Item Sent'
    OTHER = 'other', 'Other'
