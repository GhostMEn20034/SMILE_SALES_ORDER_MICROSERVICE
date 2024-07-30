from typing import Any

import requests
from django.conf import settings

from apps.payments.exceptions import (
    PaymentCreationFailedException,
    PaymentCaptureFailedException,
    PaymentRefundFailedException,
)
from services.payments.payment_params.paypal.create_paypal_payment_params import CreatePaypalPaymentParams
from utils.payments.paypal.token_managers.paypal_token_manager import PaypalTokenManager


class PayPalClient:
    """
    Responsible for interaction with the PayPal API
    """
    def __init__(self, client_id: str, client_secret: str):
        self.token_manager = PaypalTokenManager(client_id, client_secret)

    def _get_base_headers(self) -> dict[str, Any]:
        auth_token_data = self.token_manager.get_auth_token_data()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'{auth_token_data.token_type} {auth_token_data.access_token}'
        }
        return headers

    def create_payment(self, payment_params: CreatePaypalPaymentParams) -> dict:
        """
        Creates a payment with the given payment params
        """
        headers = self._get_base_headers()

        payment_data = {
            "intent": payment_params.intent,
            "purchase_units": [purchase_unit.to_dict() for purchase_unit in payment_params.purchase_units],
            "payment_source": {
                "paypal": {
                    "experience_context": payment_params.paypal_payment_source.experience_context.to_dict(),
                }
            }
        }
        order_payment_url = f"{settings.PAYPAL_API_BASE_URL}/v2/checkout/orders"

        response = requests.post(order_payment_url, headers=headers, json=payment_data)

        if response.status_code == 200:
            return response.json()

        raise PaymentCreationFailedException


    def capture_payment(self, payment_id: str):
        """
        Captures a payment to confirm a transaction of some amount of funds to the merchant
        """
        headers = self._get_base_headers()

        capture_payment_url = f"{settings.PAYPAL_API_BASE_URL}/v2/checkout/orders/{payment_id}/capture"

        response = requests.post(capture_payment_url, headers=headers)
        if response.status_code == 201:
            return response.json()

        raise PaymentCaptureFailedException

    def refund_payment(self, capture_id: str, refund_reason: str):
        headers = self._get_base_headers()
        headers["Prefer"] = "return=representation"

        refund_request_body = {
            "note_to_payer": refund_reason,
        }
        payment_refund_url = f"{settings.PAYPAL_API_BASE_URL}/v2/payments/captures/{capture_id}/refund"
        response = requests.post(payment_refund_url, headers=headers, json=refund_request_body)

        if response.status_code == 201:
            return response.json()

        raise PaymentRefundFailedException

