from rest_framework import status
from rest_framework.exceptions import APIException

class NoSellableCartItems(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'No sellable cart items were provided'
    default_code = 'no_sellable_cart_items'