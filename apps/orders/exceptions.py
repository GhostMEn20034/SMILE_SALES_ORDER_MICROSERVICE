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
