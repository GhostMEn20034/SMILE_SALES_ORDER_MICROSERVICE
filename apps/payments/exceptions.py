from rest_framework import status
from rest_framework.exceptions import APIException


class PaymentCreationFailedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Unable to create a payment"


class PaymentCaptureFailedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Unable to capture a payment"

