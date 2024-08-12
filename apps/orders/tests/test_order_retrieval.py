import uuid
from typing import List

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.addresses.models import Address
from apps.orders.exceptions import OrderDoesNotExist
from apps.products.models import Product
from testing_utils.common.test_case_setup import setup_order_api_test_case
from testing_utils.orders.order_utils import OrderTestingUtils
from testing_utils.products.product_setup import ProductSetupInitializer

path_to_payment_service = 'services.payments.payment_service.PaymentService'
path_to_order_processing_replicator = 'replicators.order_processing_replicator.OrderProcessingReplicator'
# Path to the file with dramatiq actors which send emails related to different order actions
path_to_email_sending_tasks = 'apps.orders.tasks.email_sending'


Account = get_user_model()


class TestOrderRetrieval(APITestCase):
    test_user: Account
    other_test_user: Account
    addresses: List[Address]
    products: List[Product]
    order_testing_utils: OrderTestingUtils
    # Access token that allows us to do something as test_user
    access_token: str
    # Access Token of other test user
    other_access_token: str
    # Test user's password
    password: str

    def setUp(self):
        setup_order_api_test_case(self)

    def get_products_for_order(self) -> List[Product]:
        # Guarantee that products the user want to buy are sellable
        first_product = self.products[0]
        ProductSetupInitializer.update_product_availability(first_product, 11, True)
        second_product = self.products[1]
        ProductSetupInitializer.update_product_availability(second_product, 14, True)

        return [first_product, second_product]

    def _add_authorization_header(self, access_token: str):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    def test_user_has_access_to_his_order(self):
        products = self.get_products_for_order()
        created_order = self.order_testing_utils.create_test_order(
            self.test_user, products,
            self.addresses[0].original_id,
        )

        self._add_authorization_header(self.access_token)
        get_order_url = reverse("orders-details", kwargs={"order_uuid": created_order.order_uuid})

        response = self.client.get(get_order_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["order"]["order_uuid"], str(created_order.order_uuid))

    def test_should_return_404_if_order_does_not_exist(self):
        products = self.get_products_for_order()
        self.order_testing_utils.create_test_order(
            self.test_user, products,
            self.addresses[0].original_id,
        )

        self._add_authorization_header(self.access_token)
        get_order_url = reverse("orders-details", kwargs={"order_uuid": uuid.uuid4()})

        response = self.client.get(get_order_url, format='json')
        self.assertEqual(response.status_code, OrderDoesNotExist.status_code)
        self.assertEqual(response.data["detail"], OrderDoesNotExist.default_detail)

    def test_only_owner_has_access_to_his_order(self):
        products = self.get_products_for_order()
        created_order = self.order_testing_utils.create_test_order(
            self.test_user, products,
            self.addresses[0].original_id,
        )
        # Authenticate as other test user
        self._add_authorization_header(self.other_access_token)
        get_order_url = reverse("orders-details", kwargs={"order_uuid": created_order.order_uuid})
        response = self.client.get(get_order_url)
        # The order shouldn't be found,
        # because our API finds orders by order_uuid
        # AND user_id field (which is not matching in this case)
        self.assertEqual(response.status_code, OrderDoesNotExist.status_code)
        self.assertEqual(response.data["detail"], OrderDoesNotExist.default_detail)

    def test_user_can_access_only_his_orders_in_order_list_route(self):
        products = self.get_products_for_order()
        self.order_testing_utils.create_test_order(
            self.test_user, products,
            self.addresses[0].original_id,
        )
        self._add_authorization_header(self.access_token)
        get_order_list_url = reverse("orders-list") + "?order_status=allOrders"

        response = self.client.get(get_order_list_url)
        # In this case the user should see his one order
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

        # Authenticate as other test user
        self._add_authorization_header(self.other_access_token)
        response = self.client.get(get_order_list_url)
        # Since other user doesn't have any orders, he should see 0 orders
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
