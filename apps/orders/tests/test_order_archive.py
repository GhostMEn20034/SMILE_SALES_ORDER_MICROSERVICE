from typing import List

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.addresses.models import Address
from apps.orders.models import Order
from apps.products.models import Product
from testing_utils.common.test_case_setup import setup_order_api_test_case
from testing_utils.orders.order_utils import OrderTestingUtils
from testing_utils.products.product_setup import ProductSetupInitializer

path_to_payment_service = 'services.payments.payment_service.PaymentService'
path_to_order_processing_replicator = 'replicators.order_processing_replicator.OrderProcessingReplicator'
# Path to the file with dramatiq actors which send emails related to different order actions
path_to_email_sending_tasks = 'apps.orders.tasks.email_sending'


Account = get_user_model()


class TestOrderArchive(APITestCase):
    test_user: Account
    addresses: List[Address]
    products: List[Product]
    order_testing_utils: OrderTestingUtils
    # Access token that allows us to do something as test_user
    access_token: str
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


    def _add_authorization_header(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

    def test_product_archive_with_correct_data_should_be_successful(self):
        products = self.get_products_for_order()
        created_order = self.order_testing_utils.create_test_order(
            self.test_user, products,
            self.addresses[0].original_id,
        )

        self._add_authorization_header()
        # purpose field is not specified because its default value is "archive"
        response = self.order_testing_utils.send_request_to_archive_order(order_id=created_order.order_uuid,)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_unarchive_with_correct_data_should_be_successful(self):
        products = self.get_products_for_order()
        created_order = self.order_testing_utils.create_test_order(
            self.test_user, products,
            self.addresses[0].original_id,
        )

        self._add_authorization_header()
        # purpose field is not specified because its default value is "archive"
        self.order_testing_utils.send_request_to_archive_order(order_id=created_order.order_uuid,)

        self.assertEqual(Order.objects.filter(archived=False).count(), 0)
        self.assertEqual(Order.objects.filter(archived=True).count(), 1)

        unarchive_response = self.order_testing_utils.send_request_to_archive_order(
            order_id=created_order.order_uuid, purpose="unarchive"
        )
        self.assertEqual(unarchive_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.filter(archived=False).count(), 1)
        self.assertEqual(Order.objects.filter(archived=True).count(), 0)
