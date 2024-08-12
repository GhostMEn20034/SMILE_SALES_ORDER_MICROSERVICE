import random
from decimal import Decimal

from apps.payments.models import Payment
from services.payments.payment_params.base.capture import Capture
from services.payments.payment_params.paypal.base.amount import AmountParamBase
from services.payments.payment_params.paypal.refund_breakdown import RefundBreakdown
from services.payments.payment_responses.paypal.capture_payment_response import CapturePayPalPaymentResponse
from services.payments.payment_responses.paypal.create_payment_response import CreatePaypalPaymentResponse
from services.payments.payment_responses.paypal.refund_payment_response import RefundPayPalPaymentResponse


def initialize_payment() -> CreatePaypalPaymentResponse:
    return CreatePaypalPaymentResponse(
        payment_id="5O190127TN364715T",
        status="PAYER_ACTION_REQUIRED",
        checkout_link="https://www.paypal.com/checkoutnow?token=5O190127TN364715T",
    )

def perform_payment_capture():
    payment_id = "5O190127TN364715T"
    capture_id = "3C679366HH908993F"

    # Generate random values for net_amount and provider_fee
    net_value = round(random.uniform(50.00, 100.00), 2)
    fee_value = round(random.uniform(1.00, 5.00), 2)

    net_amount = AmountParamBase(value=str(net_value), currency_code="USD")
    provider_fee = AmountParamBase(value=str(fee_value), currency_code="USD")

    # Calculate gross_amount as the sum of net_amount and provider_fee
    gross_value = round(Decimal(net_amount.value) + Decimal(provider_fee.value), 2)
    gross_amount = AmountParamBase(value=str(gross_value), currency_code="USD")

    capture = Capture(
        capture_id=capture_id, gross_amount=gross_amount,
        net_amount=net_amount, provider_fee=provider_fee,
    )

    capture_response = CapturePayPalPaymentResponse(
        payment_id=payment_id,
        captures=[capture, ]
    )
    return capture_response

def perform_payment_refund(payment: Payment, refund_reason: str) -> RefundPayPalPaymentResponse:
    refund_id = "1JU08902781691411"

    refund_breakdown = RefundBreakdown(
        gross_amount=AmountParamBase(
            value=str(payment.gross_amount),
            currency_code=payment.currency,
        ),
        provider_fee=AmountParamBase(
            value=str(payment.provider_fee),
            currency_code=payment.currency,
        ),
        net_amount=AmountParamBase(
            value=str(payment.net_amount),
            currency_code=payment.currency,
        ),
    )

    return RefundPayPalPaymentResponse(
        status="COMPLETED",
        refund_id=refund_id,
        refund_reason=refund_reason,
        refund_breakdown=refund_breakdown,
    )
