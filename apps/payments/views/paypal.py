from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from dependencies.service_dependencies.payments import get_payment_service
from param_classes.payments.capture_payment_params import CapturePaymentParams
from services.payments.payment_service import PaymentService
from apps.payments.serializers.request_body_serializers import CapturePaymentSerializer


class PayPalPaymentViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'payment_id'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payment_service: PaymentService = get_payment_service()

    def capture_paypal_payment(self, request, payment_id: str) -> Response:
        serializer = CapturePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        capture_payment_params = CapturePaymentParams(
            order_id=validated_data["order_id"],
            payment_id=payment_id,
        )
        capture_success_data = self.payment_service.perform_paypal_payment_capture(capture_payment_params)
        return Response(status=status.HTTP_200_OK, data=capture_success_data)
