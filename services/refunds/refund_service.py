from django.db.models import QuerySet

from apps.payments.models import Payment
from apps.refunds.models import Refund
from param_classes.refunds.refund_request_creation import RefundRequestCreationParams
from apps.refunds.tasks.email_sending import (
    send_email_about_refund_approval,
    send_email_about_refund_rejection,
)


class RefundService:
    def __init__(self, refund_queryset: QuerySet[Refund]):
        self.refund_queryset = refund_queryset

    def create_refund(self, params: RefundRequestCreationParams) -> Refund:
        refund: Refund = self.refund_queryset.create(
            reason_for_return=params.reason_for_return,
            user_id=params.user_id,
            order_id=params.order_id,
        )
        return refund

    @staticmethod
    def approve_refund(refund: Refund) -> Refund:
        refund.approve()
        return refund

    @staticmethod
    def reject_refund(refund: Refund, reject_reason: str) -> Refund:
        refund.reject(reject_reason)
        return refund

    @staticmethod
    def send_refund_request_rejection_email(refund: Refund) -> None:
        """
        Sends a notification email regarding the rejection
        of a refund request. It utilizes a Dramatiq actor to handle the email
        sending process asynchronously.

        :param refund: The Refund object representing the refund request that was rejected.
        The method uses the refund's ID to trigger the email sending process.
        """
        send_email_about_refund_rejection.send(refund.id)


    @staticmethod
    def send_refund_request_approval_email(refund: Refund, payment: Payment) -> None:
        """
        Sends a notification email regarding the approval
        of a refund request. It utilizes a Dramatiq actor to handle the email
        sending process asynchronously.

        :param refund: The Refund object representing the refund request that was approved.
            The method uses the refund's ID to trigger the email sending process.
        :param payment: The Payment object associated with the approved refund request.

        """
        send_email_about_refund_approval.send(refund.id, payment.id)
