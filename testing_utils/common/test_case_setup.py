from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from testing_utils.addresses.address_setup import AddressSetupInitializer
from testing_utils.auth.auth_setup import AuthSetupInitializer
from testing_utils.orders.order_utils import OrderTestingUtils
from testing_utils.products.product_setup import ProductSetupInitializer


Account = get_user_model()


def setup_order_api_test_case(test_case: APITestCase) -> None:
    """
    Performs setup steps that are common for all test cases.
    """
    test_case.password = "test1234"

    test_case.test_user = Account.objects.create_user(
        email="testing44@gmail.com",
        password=test_case.password,
        first_name="Hello",
        original_id=69,
    )

    test_case.other_test_user = Account.objects.create_user(
        email="testing2n2@gmail.com",
        password=test_case.password,
        first_name="Bye",
        original_id=102,
    )

    test_case.addresses = AddressSetupInitializer.get_addresses(test_case.test_user)
    test_case.products = ProductSetupInitializer.get_products()

    test_case.order_testing_utils = OrderTestingUtils(test_case.client)

    test_case.access_token = AuthSetupInitializer.get_auth_token(test_case.test_user)
    # Access token of other test user
    test_case.other_access_token = AuthSetupInitializer.get_auth_token(test_case.other_test_user)