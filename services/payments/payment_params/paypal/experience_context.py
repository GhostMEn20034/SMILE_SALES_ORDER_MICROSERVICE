from typing import Literal


class PayPalExperienceContext:
    """
    Customizes the payer experience during the approval process for payment with PayPal.
    PROPERTIES:
        brand_name: The label that overrides the business name in the PayPal account on the PayPal site.
        shipping_preference: The location from which the shipping address is derived.
        landing_page: The type of landing page to show on the PayPal site for customer checkout.
        user_action: Configures a Continue or Pay Now checkout flow.
        return_url: The URL where the customer will be redirected upon approving a payment.
        cancel_url: The URL where the customer will be redirected upon cancelling the payment approval.
    """
    def __init__(self, brand_name: str,
                 shipping_preference: Literal["GET_FROM_FILE", "NO_SHIPPING", "SET_PROVIDED_ADDRESS"],
                 landing_page: Literal["LOGIN", "GUEST_CHECKOUT", "NO_PREFERENCE"],
                 user_action: Literal["CONTINUE", "PAY_NOW"],
                 return_url: str, cancel_url: str, ):
        self.brand_name = brand_name
        self.shipping_preference = shipping_preference
        self.landing_page = landing_page
        self.user_action = user_action
        self.return_url = return_url
        self.cancel_url = cancel_url

    def to_dict(self) -> dict:
        return {
            'brand_name': self.brand_name,
            'shipping_preference': self.shipping_preference,
            'landing_page': self.landing_page,
            'user_action': self.user_action,
            'return_url': self.return_url,
            'cancel_url': self.cancel_url,
        }