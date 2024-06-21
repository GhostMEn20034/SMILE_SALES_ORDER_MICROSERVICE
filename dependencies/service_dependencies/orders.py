from services.orders.order_service import OrderService
from .payments import get_payment_service


def get_order_service(order_queryset) -> OrderService:
    payment_service = get_payment_service()
    return OrderService(order_queryset, payment_service)