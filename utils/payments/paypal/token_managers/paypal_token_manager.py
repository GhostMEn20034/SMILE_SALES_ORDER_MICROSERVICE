import time
import requests
from django.conf import settings
from django.core.cache import cache

from result_classes.payments.paypal_auth_token_data import PaypalAuthTokenData


class PaypalTokenManager:
    TOKEN_CACHE_KEY = 'paypal_access_token'
    TOKEN_EXPIRATION_CACHE_KEY = 'paypal_token_expires_at'
    TOKEN_TYPE_CACHE_KEY = 'paypal_token_type'

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_auth_token_data(self) -> PaypalAuthTokenData:
        access_token = cache.get(self.TOKEN_CACHE_KEY)
        token_expires_at = cache.get(self.TOKEN_EXPIRATION_CACHE_KEY)
        token_type = cache.get(self.TOKEN_TYPE_CACHE_KEY)

        # Fetch a new token if it's not present or has expired
        if not access_token or not token_expires_at or time.time() >= token_expires_at:
            self._fetch_new_access_token_data()

            access_token = cache.get(self.TOKEN_CACHE_KEY)
            token_expires_at = cache.get(self.TOKEN_EXPIRATION_CACHE_KEY)
            token_type = cache.get(self.TOKEN_TYPE_CACHE_KEY)

        return PaypalAuthTokenData(access_token, token_expires_at, token_type)

    def _fetch_new_access_token_data(self):
        url = f"{settings.PAYPAL_API_BASE_URL}/v1/oauth2/token"
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en_US",
        }
        data = {
            "grant_type": "client_credentials"
        }
        response = requests.post(url, headers=headers, data=data,
                                 auth=(self.client_id, self.client_secret))

        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data['access_token']
            expires_in = token_data['expires_in']

            cache.set(self.TOKEN_CACHE_KEY, access_token, timeout=expires_in)
            cache.set(self.TOKEN_EXPIRATION_CACHE_KEY, time.time() + expires_in, timeout=expires_in)
            cache.set(self.TOKEN_TYPE_CACHE_KEY, token_data['token_type'], timeout=expires_in)
        else:
            raise Exception(f"Failed to obtain access token: {response.text}")
