from rest_framework import status
from rest_framework.exceptions import APIException


class PaymentCreationFailedException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Unable to create a payment"


class PaymentCaptureFailedException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Unable to capture a payment"


class PaymentRefundFailedException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Unable to refund a payment"


class PaymentToRefundNotFoundException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Unable to refund a payment, since the payment is not found"
