from typing import Dict


class OrderConfirmationData:
    def __init__(self, payment: Dict):
        self.payment = payment
