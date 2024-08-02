from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from dependencies.mediator_dependencies.order_processing import get_order_processing_coordinator
from mediators.order_processing_coordinator import OrderProcessingCoordinator
from param_classes.refunds.refund_request_creation import RefundRequestCreationParams
from .serializers.request_body import CreateRefundSerializer


class RefundsViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_processing_coordinator: OrderProcessingCoordinator = get_order_processing_coordinator()

    def create_refund_request(self, request, *args, **kwargs) -> Response:
        serializer = CreateRefundSerializer(data={
            "user_id": request.user.id,
            **request.data,
        })
        serializer.is_valid(raise_exception=True)
        refund_creation_params = RefundRequestCreationParams(**serializer.validated_data)
        self.order_processing_coordinator.create_refund_request(refund_creation_params)

        return Response(status=status.HTTP_201_CREATED)
