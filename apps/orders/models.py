import uuid
from django.contrib.auth import get_user_model
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
        ('cancelled', 'Cancelled')
    ]

    order_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='original_id')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, to_field='original_id', null=True)
    status = models.CharField(max_length=10, choices=order_status_choices, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order № {self.order_uuid} created by {self.user.email}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, to_field='order_uuid')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field="object_id")
    price_per_unit = models.DecimalField(max_digits=13, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    amount = models.GeneratedField(
        expression=F('price_per_unit') * F('quantity'),
        output_field=models.DecimalField(max_digits=13, decimal_places=2),
        db_persist=True,
    )

    def __str__(self):
        return f'Order №{self.order_id}, {self.product.name} x {self.quantity}'
