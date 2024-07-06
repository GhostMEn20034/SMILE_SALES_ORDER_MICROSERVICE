from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from apps.orders.serializers.request_body_serializers import OrderCreationRequestBody
from dependencies.service_dependencies.orders import get_order_service
from dependencies.mediator_dependencies.order_processing import get_order_processing_coordinator
from mediators.order_processing_coordinator import OrderProcessingCoordinator
from services.orders.order_service import OrderService
from param_classes.order_processing_coordinator.order_creation import OrderCreationParams


class OrderViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_service: OrderService = get_order_service()
        self.order_processing_coordinator: OrderProcessingCoordinator = get_order_processing_coordinator(
            order_service=self.order_service)

    def create(self, request, *args, **kwargs):
        print(request.data)

        serializer = OrderCreationRequestBody(data={
            'cart_owner_id': request.user.id,
            'address_id': request.data['address_id'],
            'product_ids': request.data['product_ids'],
        })
        serializer.is_valid(raise_exception=True)

        order_creation_params: OrderCreationParams = OrderCreationParams(**serializer.validated_data)
        payment_data = self.order_processing_coordinator.create_order_and_initialize_payment(order_creation_params)
        return Response(
            data={
                'payment_id': payment_data.payment_id,
                'checkout_link': payment_data.checkout_link,
            },
            status=status.HTTP_201_CREATED,
        )

    def get_order_creation_essentials(self, request, *args, **kwargs):
        order_creation_essentials = self.order_processing_coordinator.get_order_creation_essentials(
            user_id=request.user.id,
        )
        return Response(
            data={
                "addresses": order_creation_essentials.addresses,
            },
            status=status.HTTP_200_OK,
        )
