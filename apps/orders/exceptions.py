from rest_framework import status
from rest_framework.exceptions import APIException


class OrderDoesNotExist(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Order with specified identifier does not exist'
    default_code = 'order_does_not_exist'


class TooMuchArchivedOrders(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'You cannot archive more than 250 orders'
    default_code = 'too_much_archived_orders'


class OrderAlreadyCanceled(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Order is already canceled'
    default_code = 'order_already_canceled'


class OrderIsFinalized(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Not able to cancel the order is already finalized'
    default_code = 'order_is_finalized'

class OrderIsShipping:
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Order is in shipping process'
    default_code = 'order_is_shipping'
