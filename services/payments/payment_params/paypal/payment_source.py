from .experience_context import PayPalExperienceContext

class PayPalPaymentSource:
    def __init__(self, experience_context: PayPalExperienceContext):
        self.experience_context = experience_context
