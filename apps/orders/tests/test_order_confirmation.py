import uuid
from typing import List
from unittest import mock
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.addresses.models import Address
from apps.products.models import Product
from testing_utils.orders.order_utils import OrderTestingUtils
from testing_utils.common.test_case_setup import setup_order_api_test_case
from testing_utils.payments.payment_service_mocked_responses import perform_payment_capture
from testing_utils.products.product_setup import ProductSetupInitializer
from apps.orders.exceptions import OrderDoesNotExist, PendingOrdersOnlyEligibleToBeProcessed

path_to_payment_service = 'services.payments.payment_service.PaymentService'
path_to_order_processing_replicator = 'replicators.order_processing_replicator.OrderProcessingReplicator'

Account = get_user_model()


class TestOrderConfirmation(APITestCase):
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

    def _add_authorization_header(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

    @mock.patch('apps.orders.tasks.email_sending.send_email_with_order_confirmation.send')
    @mock.patch(path_to_payment_service + '.perform_payment_capture')
    def test_attempt_of_confirming_existing_non_processed_order_should_be_successful(
            self, mocked_payment_capture, mocked_email_sending):
        mocked_payment_capture.return_value = perform_payment_capture()

        # Guarantee that products the user want to buy are sellable
        first_product = self.products[0]
        ProductSetupInitializer.update_product_availability(first_product, 8, True)
        second_product = self.products[1]
        ProductSetupInitializer.update_product_availability(second_product, 9, True)

        self._add_authorization_header()

        response = self.order_testing_utils.create_unconfirmed_order(self.test_user,
                                                                     [first_product, second_product],
                                                                     self.addresses[0].original_id,
                                                                     )
        payment_confirmation_response = self.order_testing_utils.send_request_to_confirm_order(
            response.data["order_id"], response.data["payment_id"],
        )
        # Assert that request status is HTTP 200
        self.assertEqual(payment_confirmation_response.status_code, status.HTTP_200_OK)
        # Assert that payment status is success
        self.assertEqual(payment_confirmation_response.data["payment_status"], "success")
        # Assert that email sending has been called
        self.assertTrue(mocked_email_sending.called)

    @mock.patch('apps.orders.tasks.email_sending.send_email_with_order_confirmation.send')
    @mock.patch(path_to_payment_service + '.perform_payment_capture')
    def test_attempt_of_confirming_non_existing_order_should_fail(self, mocked_payment_capture, mocked_email_sending):
        mocked_payment_capture.return_value = perform_payment_capture()

        # Guarantee that products the user want to buy are sellable
        first_product = self.products[0]
        ProductSetupInitializer.update_product_availability(first_product, 10, True)
        second_product = self.products[1]
        ProductSetupInitializer.update_product_availability(second_product, 15, True)

        self._add_authorization_header()

        response = self.order_testing_utils.create_unconfirmed_order(self.test_user,
                                                                     [first_product, second_product],
                                                                     self.addresses[0].original_id,
                                                                     )

        payment_confirmation_response = self.order_testing_utils.send_request_to_confirm_order(
            uuid.uuid4(), response.data["payment_id"],
        )
        # Assert that order has not been found
        self.assertEqual(payment_confirmation_response.status_code, status.HTTP_404_NOT_FOUND)
        # Assert that correct exception has been raised
        self.assertEqual(payment_confirmation_response.data["detail"], OrderDoesNotExist.default_detail)

        # Assert that email sending has been called
        self.assertFalse(mocked_email_sending.called)

    @mock.patch('apps.orders.tasks.email_sending.send_email_with_order_confirmation.send')
    @mock.patch(path_to_payment_service + '.perform_payment_capture')
    def test_attempt_of_confirming_existing_not_pending_order_should_fail(
            self, mocked_payment_capture, mocked_email_sending):
        mocked_payment_capture.return_value = perform_payment_capture()

        # Guarantee that products the user want to buy are sellable
        first_product = self.products[0]
        ProductSetupInitializer.update_product_availability(first_product, 11, True)
        second_product = self.products[1]
        ProductSetupInitializer.update_product_availability(second_product, 89, True)

        self._add_authorization_header()

        response = self.order_testing_utils.create_unconfirmed_order(self.test_user,
                                                                     [first_product, second_product],
                                                                     self.addresses[0].original_id,
                                                                     )
        # Confirm the request
        self.order_testing_utils.send_request_to_confirm_order(
            response.data["order_id"], response.data["payment_id"],
        )
        # Assert that email sending has been called
        self.assertTrue(mocked_email_sending.called)
        # Now, trying to confirm the order again
        response = self.order_testing_utils.send_request_to_confirm_order(
            response.data["order_id"], response.data["payment_id"],
        )
        # The request should fail because the order is already processed
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], PendingOrdersOnlyEligibleToBeProcessed.default_detail)
        # Assert that email sending has been called only once (Before the failed request)
        self.assertEqual(mocked_email_sending.call_count, 1)
