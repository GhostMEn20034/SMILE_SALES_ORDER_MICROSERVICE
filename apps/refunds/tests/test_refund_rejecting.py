from typing import List
from unittest import mock

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.addresses.models import Address
from apps.products.models import Product
from apps.refunds.models import Refund
from dependencies.mediator_dependencies.order_processing import get_order_processing_coordinator
from testing_utils.common.test_case_setup import setup_order_api_test_case
from testing_utils.orders.order_utils import OrderTestingUtils
from testing_utils.products.product_setup import ProductSetupInitializer
from testing_utils.refunds.refund_utils import RefundTestingUtils

path_to_payment_service = 'services.payments.payment_service.PaymentService'
path_to_order_processing_replicator = 'replicators.order_processing_replicator.OrderProcessingReplicator'
# Path to the file with dramatiq actors which send emails related to different order actions
path_to_email_sending_tasks = 'apps.refunds.tasks.email_sending'


Account = get_user_model()


class TestRefundRejecting(APITestCase):
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

    def _add_authorization_header(self, access_token: str):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    def get_products_for_order(self) -> List[Product]:
        # Guarantee that products the user want to buy are sellable
        first_product = self.products[0]
        ProductSetupInitializer.update_product_availability(first_product, 11, True)
        second_product = self.products[1]
        ProductSetupInitializer.update_product_availability(second_product, 14, True)

        return [first_product, second_product]

    @mock.patch(path_to_email_sending_tasks + '.send_email_about_refund_rejection.send')
    def test_refund_rejecting_should_succeed(self, mocked_refund_rejecting_email_send: mock.Mock):
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

        refund = RefundTestingUtils.create_refund(
            self.test_user.original_id,
            created_order.order_uuid,
            "not_as_described",
        )

        order_processing_coordinator = get_order_processing_coordinator()
        order_processing_coordinator.reject_refund_request(refund, "Some really important reason for rejection")
        # Email should be sent, because everything is fine
        mocked_refund_rejecting_email_send.assert_called()
        # Refresh refund request data
        refund = Refund.objects.get(id=refund.id)
        # Ensure that refund request's status is changed
        self.assertEqual(refund.status, "rejected")