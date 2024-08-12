from abc import ABC, abstractmethod
from typing import Optional

from apps.payments.models import Payment
from param_classes.payments.capture_payment_params import CapturePaymentParams
from param_classes.payments.initialize_payment import InitializePaymentParams
from param_classes.payments.payment_creation import PaymentCreationParams
from param_classes.payments.refund_creation import RefundCreationParams


class AbstractPaymentService(ABC):
    @abstractmethod
    def create_payment(self, params: PaymentCreationParams) -> Optional[Payment]:
        """
        Creates a payment object, inserts it into the db, and returns it.
        """
        pass

    @abstractmethod
    def initialize_payment(self, params: InitializePaymentParams):
        """
        Initializes a payment (Creates in the payment gateway, but doesn't create in the db).
        """
        pass

    @abstractmethod
    def perform_payment_capture(self, data: CapturePaymentParams):
        """
        Captures the payment.
        """
        pass

    @abstractmethod
    def create_refund(self, params: RefundCreationParams) -> Optional[Payment]:
        """
        Creates a payment object with "refund" type in the database and returns it.
        """
        pass

    @abstractmethod
    def perform_payment_refund(self, payment: Payment, refund_reason: str):
        """
        Performs a full payment refund.
        """
        pass