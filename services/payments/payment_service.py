from typing import Optional

from django.conf import settings
from django.db.models import QuerySet

from apps.payments.models import Payment
from apps.payments.serializers.api_serializers import PaymentSerializer
from param_classes.payments.build_purchase_unit_params import BuildPurchaseUnitParams
from param_classes.payments.capture_payment_params import CapturePaymentParams
from param_classes.payments.initialize_payment import InitializePaymentParams
from param_classes.payments.payment_creation import PaymentCreationParams
from param_classes.payments.refund_creation import RefundCreationParams
from utils.payments.paypal.response_parsers.payment_capture_response_parser import PayPalCaptureResponseParser
from utils.payments.paypal.response_parsers.payment_refund_response_parser import PaymentRefundResponseParser
from .payment_clients.paypal import PayPalClient
from .payment_params.paypal.create_paypal_payment_params import CreatePaypalPaymentParams
from .payment_params.paypal.payment_source import PayPalPaymentSource
from .payment_params.paypal.experience_context import PayPalExperienceContext
from .payment_params.paypal.payment_params_preparer import PayPalPaymentParamsPreparer
from .payment_responses.paypal.capture_payment_response import CapturePayPalPaymentResponse
from .payment_responses.paypal.create_payment_response import CreatePaypalPaymentResponse
from .payment_responses.paypal.refund_payment_response import RefundPayPalPaymentResponse


class PaymentService:
    def __init__(self, payment_queryset: QuerySet[Payment]):
        self.paypal_client = PayPalClient(
            settings.PAYPAL_CLIENT_ID,
            settings.PAYPAL_SECRET,
        )
        self.payment_queryset = payment_queryset

    def create_payment(self, params: PaymentCreationParams) -> Optional[Payment]:
        """
        Creates a payment object, inserts it into the db and returns it
        """
        serializer = PaymentSerializer(data={
            "user": params.user_id,
            "order": params.order_id,
            "net_amount": params.capture.net_amount.value,
            "provider_fee": params.capture.provider_fee.value,
            "currency": params.capture.net_amount.currency_code,
            "status": params.status,
            "provider": params.provider,
            "provider_payment_id": params.payment_id,
            "capture_id": params.capture.capture_id,
        })
        if not serializer.is_valid():
            return None

        payment: Payment = self.payment_queryset.create(**serializer.validated_data)
        return payment

    def initialize_paypal_payment(self, params: InitializePaymentParams) -> CreatePaypalPaymentResponse:
        """
        Initialize (Create in PayPal, but don't create in ours db) a PayPal payment
        """
        build_purchase_unit_params = BuildPurchaseUnitParams(
            reference_id=str(params.created_order.order.order_uuid),
            description="Order in Smile Sales",
            order_items=params.created_order.order_items,
            currency_code=params.created_order.order.currency,
        )

        purchase_unit = PayPalPaymentParamsPreparer.build_purchase_unit(build_purchase_unit_params)
        experience_context = PayPalExperienceContext(
            brand_name="Smile Sales",
            shipping_preference="NO_SHIPPING",
            landing_page="LOGIN",
            user_action="PAY_NOW",
            return_url=f"{settings.FRONTEND_BASE_URL}/payments/success"
                       f"?orderId={purchase_unit.reference_id}"
                       f"&orderDate={str(params.created_order.order.created_at.date())}"
                       f"&paymentMethod=paypal",
            cancel_url=f"{settings.FRONTEND_BASE_URL}/payments/canceled"
                       f"?orderId={purchase_unit.reference_id}"
                       f"&paymentMethod=paypal",
        )
        payment_source = PayPalPaymentSource(experience_context)

        create_payment_params = CreatePaypalPaymentParams(
            intent="CAPTURE",
            purchase_units=[purchase_unit, ],
            paypal_payment_source=payment_source,
        )

        created_payment_data = self.paypal_client.create_payment(create_payment_params)

        checkout_link = next((link['href'] for link in created_payment_data['links']
                              if link['rel'] == 'payer-action'), None)

        create_order_response = CreatePaypalPaymentResponse(
            payment_id=created_payment_data['id'],
            status=created_payment_data['status'],
            checkout_link=checkout_link,
        )

        return create_order_response

    def perform_paypal_payment_capture(self, data: CapturePaymentParams) -> CapturePayPalPaymentResponse:
        """
        Captures PayPal Payment
        """
        capture_data = self.paypal_client.capture_payment(data.payment_id)
        capture_response_parser = PayPalCaptureResponseParser(capture_data)
        capture_response = capture_response_parser.parse()

        return capture_response

    def create_refund(self, params: RefundCreationParams) -> Optional[Payment]:
        """
        Creates a payment object with "refund" type in the database and returns it
        """
        serializer = PaymentSerializer(data={
            "user": params.user_id,
            "order": params.order_id,
            "net_amount": params.refund_breakdown.net_amount.value,
            "provider_fee": params.refund_breakdown.provider_fee.value,
            "currency": params.refund_breakdown.net_amount.currency_code,
            "status": params.status,
            "provider": params.provider,
            "provider_payment_id": params.refund_id,
            "type": "refund",
        })

        if not serializer.is_valid():
            return None

        payment: Payment = self.payment_queryset.create(**serializer.validated_data)
        return payment

    def perform_paypal_payment_refund(self, payment: Payment, refund_reason: str) -> RefundPayPalPaymentResponse:
        """
        Performs full payment refund
        """
        refund_data = self.paypal_client.refund_payment(payment.capture_id, refund_reason)
        refund_response_parser = PaymentRefundResponseParser(refund_data)
        parsed_refund_response = refund_response_parser.parse()
        return parsed_refund_response
