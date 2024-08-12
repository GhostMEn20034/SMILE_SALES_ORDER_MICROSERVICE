from typing import TypedDict
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


Account = get_user_model()


class _AuthTokens(TypedDict):
    refresh: str
    access: str


class TokenRetriever:

    @staticmethod
    def retrieve_tokens(account: Account) -> _AuthTokens:
        refresh = RefreshToken.for_user(account)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

