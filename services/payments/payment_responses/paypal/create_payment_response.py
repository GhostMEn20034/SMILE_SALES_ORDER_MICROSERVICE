class CreatePaypalPaymentResponse:
    def __init__(self, payment_id: str, status: str, checkout_link: str):
        self.payment_id = payment_id
        self.status = status
        self.checkout_link = checkout_link
