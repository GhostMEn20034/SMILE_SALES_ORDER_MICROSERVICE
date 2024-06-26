from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.orders.models import Order
from dependencies.service_dependencies.orders import get_order_service
from services.orders.order_service import OrderService


class OrderViewSet(viewsets.ViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Order.objects.all()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_service: OrderService = get_order_service(self.queryset)

    def create(self, request):
        payment_data = self.order_service.create_order()
        return Response(
            data={
                'payment_id': payment_data.payment_id,
                'checkout_link': payment_data.checkout_link,
            },
            status=status.HTTP_201_CREATED,
        )
