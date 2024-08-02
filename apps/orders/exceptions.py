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


class OrderIsCompleted(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Not able to cancel the order is already completed'
    default_code = 'order_is_completed'

class OrderIsShipping(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Order is in shipping process'
    default_code = 'order_is_shipping'

class DeliveredOrdersOnlyEligibleForRefundException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Only delivered orders are eligible for refunds'
    default_code = 'delivered_orders_only_eligible_for_refund'