from django.contrib.auth import get_user_model

from .token_retriever import TokenRetriever


Account = get_user_model()


class AuthSetupInitializer:

    @staticmethod
    def get_auth_token(account: Account) -> str:
        tokens = TokenRetriever.retrieve_tokens(account)
        return tokens["access"]

