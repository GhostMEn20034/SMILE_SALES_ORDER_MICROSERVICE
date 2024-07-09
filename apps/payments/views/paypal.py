from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from dependencies.mediator_dependencies.order_processing import get_order_processing_coordinator
from dependencies.service_dependencies.payments import get_payment_service
from mediators.order_processing_coordinator import OrderProcessingCoordinator
from param_classes.payments.capture_payment_params import CapturePaymentParams
from services.payments.payment_service import PaymentService
from apps.payments.serializers.request_body_serializers import CapturePaymentSerializer


class PayPalPaymentViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'payment_id'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payment_service: PaymentService = get_payment_service()
        self.order_processing_coordinator: OrderProcessingCoordinator = get_order_processing_coordinator(
            payment_service=self.payment_service)

    def capture_payment(self, request, payment_id: str) -> Response:
        serializer = CapturePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        capture_payment_params = CapturePaymentParams(
            order_id=validated_data["order_id"],
            payment_id=payment_id,
            user_id=request.user.id,
            provider='paypal',
        )
        capture_success_data = self.order_processing_coordinator.complete_funds_transferring(capture_payment_params)
        return Response(
            status=status.HTTP_200_OK,
            data={
                "payment_id": capture_success_data.provider_payment_id,
                "order_id": capture_success_data.order_id,
                "payment_status": capture_success_data.status,
                "payment_type": capture_success_data.type,
            }
        )
