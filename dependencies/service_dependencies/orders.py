from apps.orders.models import Order, OrderItem
from services.orders.order_service import OrderService


def get_order_service() -> OrderService:
    order_queryset = Order.objects.all()
    order_item_queryset = OrderItem.objects.all()

    return OrderService(order_queryset, order_item_queryset)