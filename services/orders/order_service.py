import uuid
from typing import Dict, Optional

from django.db import transaction
from django.db.models import QuerySet, Prefetch, Sum, F

from apps.orders.exceptions import OrderDoesNotExist, TooMuchArchivedOrders
from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from param_classes.orders.change_archived_status import ChangeArchivedStatusParams
from param_classes.orders.create_order import CreateOrderParams
from param_classes.orders.order_list import OrderListParams
from result_classes.orders.create_order import CreateOrderResult
from services.orders.order_list_filters.order_list_filters_generator import OrderListFiltersGenerator
from services.orders.order_list_filters.order_list_filters_resolver import OrderListFiltersResolver


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

    def get_orders(self, params: OrderListParams) -> QuerySet[Order]:
        """
        Returns all user's orders with some search criteria
        """
        filter_resolver = OrderListFiltersResolver(
            order_status=params.order_status,
            time_filter=params.time_filter,
        )
        order_status_filter = filter_resolver.resolve_order_status()
        time_filters = filter_resolver.resolve_time_filter()
        time_filters['archived'] = time_filters.get('archived', False)

        orders = self.order_queryset.filter(user_id=params.user_id, **order_status_filter, **time_filters) \
            .select_related('address').prefetch_related(
            Prefetch('order_items', queryset=self.order_items_queryset.select_related('product'))
        ).annotate(
            # Total amount's formula - SUM(amount + (tax_per_unit * quantity)),
            total_amount=Sum(F('order_items__amount') + (F('order_items__tax_per_unit') * F('order_items__quantity')))
        ).order_by('-created_at')

        return orders

    @staticmethod
    def get_order_list_filters(order_status: str) -> Optional[Dict[str, str]]:
        """
        Returns filters to filter order list by timeframe
        """
        filter_generator = OrderListFiltersGenerator(order_status)
        return filter_generator.get_filters()

    def get_order_details(self, user_id: int, order_uuid: uuid.UUID) -> Order:
        try:
            order: Order = self.order_queryset.select_related('address').prefetch_related(
                Prefetch('order_items', queryset=self.order_items_queryset.select_related('product'))
            ).prefetch_related('payments').annotate(
                total_amount_before_tax=Sum(F('order_items__amount')),
                total_tax = Sum(F('order_items__tax_per_unit') * F('order_items__quantity')),
            ).get(user_id=user_id, order_uuid=order_uuid)
        except Order.DoesNotExist:
            raise OrderDoesNotExist

        return order

    def change_archived_flag(self, params: ChangeArchivedStatusParams) -> Order:
        """
        Sets Order's "archived" field to opposite value and returns modified order object
        """
        if params.purpose == 'archive':
            archived_orders = Order.objects.filter(user_id=params.user_id, archived=True).count()
            if archived_orders >= 250:
                raise TooMuchArchivedOrders

        try:
            order: Order = self.order_queryset.get(user_id=params.user_id, order_uuid=params.order_uuid)
        except Order.DoesNotExist:
            raise OrderDoesNotExist

        archived_flag = True if params.purpose == 'archive' else False

        order.archived = archived_flag
        order.save()

        return order
