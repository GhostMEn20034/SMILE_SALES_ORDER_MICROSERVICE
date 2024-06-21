import requests
from django.conf import settings

from services.payments.payment_params.paypal.create_paypal_payment_params import CreatePaypalPaymentParams
from utils.payments.token_managers.paypal_token_manager import PaypalTokenManager


class PayPalClient:
    def __init__(self, client_id: str, client_secret: str):
        self.token_manager = PaypalTokenManager(client_id, client_secret)

    def create_payment(self, payment_params: CreatePaypalPaymentParams):
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
        else:
            return {}
        
