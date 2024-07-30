from typing import Iterable, List

from django.db.models import QuerySet, When, Case, F

from apps.orders.models import OrderItem
from apps.products.models import Product


class ProductService:
    def __init__(self, product_queryset: QuerySet[Product]):
        self.product_queryset = product_queryset

    @staticmethod
    def _create_when_statements(order_items: Iterable[OrderItem], operation: str) -> List[When]:
        """
        Creates a list of `When` conditions for the bulk update
        """
        if operation == 'reserve':
            return [
                When(object_id=order_item.product_id, then=F('stock') - order_item.quantity)
                for order_item in order_items
            ]
        elif operation == 'release':
            return [
                When(object_id=order_item.product_id, then=F('stock') + order_item.quantity)
                for order_item in order_items
            ]
        else:
            raise ValueError("Invalid operation. Must be 'reserve' or 'release'.")

    def _bulk_update_stock(self, order_items: Iterable[OrderItem], when_statements: List[When]) -> None:
        """
        Performs the bulk update for the product stock
        """
        self.product_queryset.filter(
            object_id__in=[order_item.product_id for order_item in order_items]
        ).update(
            stock=Case(*when_statements)
        )

    def reserve_for_order(self, order_items: Iterable[OrderItem]) -> None:
        """
        Reserves ordered products
        """
        when_statements = self._create_when_statements(order_items, 'reserve')
        self._bulk_update_stock(order_items, when_statements)

    def release_from_order(self, order_items: Iterable[OrderItem]) -> None:
        """
        Returns ordered products from the reservation for the order
        """
        when_statements = self._create_when_statements(order_items, 'release')
        self._bulk_update_stock(order_items, when_statements)
