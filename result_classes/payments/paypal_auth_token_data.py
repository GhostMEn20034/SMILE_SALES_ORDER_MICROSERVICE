class PaypalAuthTokenData:
    """
    Represents the data about PayPal auth token
    """
    def __init__(self, access_token: str, token_expiration: float, token_type: str):
        self.access_token = access_token
        self.token_expiration = token_expiration
        self.token_type = token_type
