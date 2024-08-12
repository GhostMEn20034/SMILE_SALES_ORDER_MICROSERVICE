import uuid
from typing import List
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.addresses.models import Address
from apps.orders.exceptions import DeliveredOrdersOnlyEligibleForRefundException, OrderDoesNotExist
from apps.products.models import Product
from testing_utils.common.test_case_setup import setup_order_api_test_case
from testing_utils.orders.order_utils import OrderTestingUtils
from testing_utils.products.product_setup import ProductSetupInitializer

path_to_payment_service = 'services.payments.payment_service.PaymentService'
path_to_order_processing_replicator = 'replicators.order_processing_replicator.OrderProcessingReplicator'
# Path to the file with dramatiq actors which send emails related to different order actions
path_to_email_sending_tasks = 'apps.orders.tasks.email_sending'


Account = get_user_model()


class TestRefundCreating(APITestCase):
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

    def test_creating_refund_request_with_correct_data_should_be_succeed(self):
        products = self.get_products_for_order()
        created_order = self.order_testing_utils.create_test_order(
            self.test_user, products,
            self.addresses[0].original_id,
        )
        # Simulating shipment process
        created_order.status = "shipped"
        created_order.save()
        # Simulating delivery process
        created_order.status = "delivered"
        created_order.save()

        self._add_authorization_header(self.access_token)

        create_refund_url = reverse('refunds-list')
        response = self.client.post(
            create_refund_url,
            data={
                "reason_for_return": "not_as_described",
                "order_id": created_order.order_uuid,
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creating_refund_request_with_not_delivered_order_should_be_failed(self):
        products = self.get_products_for_order()
        created_order = self.order_testing_utils.create_test_order(
            self.test_user, products,
            self.addresses[0].original_id,
        )
        # Simulating shipment process
        created_order.status = "shipped"
        created_order.save()
        # Don't simulate delivery process to check behaviour when the order is not delivered

        self._add_authorization_header(self.access_token)

        create_refund_url = reverse('refunds-list')
        response = self.client.post(
            create_refund_url,
            data={
                "reason_for_return": "not_as_described",
                "order_id": created_order.order_uuid,
            },
            format='json'
        )

        self.assertEqual(response.status_code, DeliveredOrdersOnlyEligibleForRefundException.status_code)
        self.assertEqual(response.data["detail"], DeliveredOrdersOnlyEligibleForRefundException.default_detail)

    def test_creating_refund_request_with_not_existing_order_should_be_failed(self):
        self._add_authorization_header(self.access_token)

        create_refund_url = reverse('refunds-list')
        response = self.client.post(
            create_refund_url,
            data={
                "reason_for_return": "not_as_described",
                "order_id": uuid.uuid4(),
            },
            format='json'
        )

        self.assertEqual(response.status_code, OrderDoesNotExist.status_code)
        self.assertEqual(response.data["detail"], OrderDoesNotExist.default_detail)


    def test_creating_refund_request_with_other_user_order_should_be_failed(self):
        """
        The user cannot create the refund request with order where he's not an owner.
        """
        products = self.get_products_for_order()
        created_order = self.order_testing_utils.create_test_order(
            self.test_user, products,
            self.addresses[0].original_id,
        )
        # Simulating shipment process
        created_order.status = "shipped"
        created_order.save()
        # Simulating delivery process
        created_order.status = "delivered"
        created_order.save()

        # Authenticate as not an owner of the order
        self._add_authorization_header(self.other_access_token)

        create_refund_url = reverse('refunds-list')
        response = self.client.post(
            create_refund_url,
            data={
                "reason_for_return": "not_as_described",
                "order_id": created_order.order_uuid,
            },
            format='json'
        )
        # The order won't be found,
        # because our server finds the order by order_uuid AND user_id (which is not matching in this case)
        self.assertEqual(response.status_code, OrderDoesNotExist.status_code)
        self.assertEqual(response.data["detail"], OrderDoesNotExist.default_detail)
