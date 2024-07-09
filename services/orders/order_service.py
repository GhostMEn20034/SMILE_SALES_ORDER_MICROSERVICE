import uuid

from django.db import transaction
from django.db.models import QuerySet

from apps.orders.models import Order, OrderItem
from param_classes.orders.create_order import CreateOrderParams
from result_classes.orders.create_order import CreateOrderResult


class OrderService:
    def __init__(self, order_queryset: QuerySet[Order], order_items_queryset: QuerySet[OrderItem]):
        self.order_queryset = order_queryset
        self.order_items_queryset = order_items_queryset

    def create_order(self, params: CreateOrderParams) -> CreateOrderResult:
        with transaction.atomic():
            order: Order = self.order_queryset.create(user_id=params.user_id, address_id=params.address_id)
            # Make Order Items Bulk Insert
            order_items = []
            for cart_item in params.cart_items:
                order_item = OrderItem(
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price_per_unit=cart_item.product.discounted_price,
                    order=order,
                    tax_rate=cart_item.product.tax_rate,
                )
                order_items.append(order_item)

            self.order_items_queryset.bulk_create(order_items)

            # Fetch the order items again with their related products
            # so generated data (AutoFields, GeneratedFields) was available
            order_items = self.order_items_queryset.filter(order=order).select_related('product')

            return CreateOrderResult(
                order=order,
                order_items=order_items,
            )

    def cancel_order(self, order_uuid: uuid.UUID) -> Order:
        """
        Sets Order's status to "canceled" and return modified order object
        """
        order: Order = self.order_queryset.get(order_uuid=order_uuid)
        order.status = "cancelled"
        order.save()
        return order

    def process_order(self, order_uuid: uuid.UUID) -> Order:
        """
        Sets Order's status to "processed" and return modified order object
        """
        order: Order = self.order_queryset.get(order_uuid=order_uuid)
        order.status = "processed"
        order.save()
        return order
