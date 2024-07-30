import uuid
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import F

from apps.addresses.models import Address
from apps.products.models import Product


User = get_user_model()


class Order(models.Model):
    order_status_choices = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ]

    order_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='original_id')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, to_field='original_id', null=True)
    status = models.CharField(max_length=10, choices=order_status_choices, default='pending', db_index=True)
    is_abandoned = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def is_canceled(self) -> bool:
        return self.status == 'cancelled'

    def is_finalized(self) -> bool:
        final_statuses = ['delivered', 'returned']
        return self.status in final_statuses

    def is_shipped(self) -> bool:
        return self.status == 'shipped'

    def is_pending(self) -> bool:
        return self.status == 'pending'

    def is_processed(self) -> bool:
        return self.status == 'processed'


    def __str__(self):
        return f'Order № {self.order_uuid} created by {self.user.email}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, to_field='order_uuid', related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field="object_id")
    price_per_unit = models.DecimalField(max_digits=13, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    tax_rate = models.DecimalField(max_digits=3, decimal_places=2, validators=[
        MinValueValidator(Decimal(0)),
        MaxValueValidator(Decimal(1))
    ], default=Decimal('0.00'))
    # Tax amount per unit
    tax_per_unit = models.GeneratedField(
        expression=F('price_per_unit') * F('tax_rate'),
        output_field=models.DecimalField(max_digits=13, decimal_places=2),
        db_persist=True,
    )
    quantity = models.PositiveIntegerField(default=1)
    amount = models.GeneratedField(
        expression=F('price_per_unit') * F('quantity'),
        output_field=models.DecimalField(max_digits=13, decimal_places=2),
        db_persist=True,
    )

    @property
    def amount_with_tax(self):
        return round(self.amount + (self.tax_per_unit * self.quantity), 2)

    def __str__(self):
        return f'Order №{self.order_id}, {self.product.name} x {self.quantity}'
