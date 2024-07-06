import requests
from django.conf import settings

from apps.payments.exceptions import PaymentCreationFailedException, PaymentCaptureFailedException
from services.payments.payment_params.paypal.create_paypal_payment_params import CreatePaypalPaymentParams
from utils.payments.token_managers.paypal_token_manager import PaypalTokenManager


class PayPalClient:
    """
    Responsible for interaction with the PayPal API
    """
    def __init__(self, client_id: str, client_secret: str):
        self.token_manager = PaypalTokenManager(client_id, client_secret)

    def create_payment(self, payment_params: CreatePaypalPaymentParams) -> dict:
        """
        Creates a payment with the given payment params
        """
        auth_token_data = self.token_manager.get_auth_token_data()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'{auth_token_data.token_type} {auth_token_data.access_token}'
        }

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

        print(response.json())
        if response.status_code == 200:
            return response.json()

        raise PaymentCreationFailedException


    def capture_payment(self, payment_id: str):
        """
        Captures a payment to confirm a transaction of some amount of funds to the merchant
        """
        auth_token_data = self.token_manager.get_auth_token_data()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'{auth_token_data.token_type} {auth_token_data.access_token}'
        }

        capture_payment_url = f"{settings.PAYPAL_API_BASE_URL}/v2/checkout/orders/{payment_id}/capture"

        response = requests.post(capture_payment_url, headers=headers)
        if response.status_code == 201:
            return response.json()
        else:
            raise PaymentCaptureFailedException
