from typing import List
from unittest import mock
from unittest.mock import Mock

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.addresses.models import Address
from apps.orders.exceptions import OrderAlreadyCanceled, OrderIsCompleted
from apps.orders.models import Order
from apps.products.models import Product
from testing_utils.common.test_case_setup import setup_order_api_test_case
from testing_utils.orders.order_utils import OrderTestingUtils
from testing_utils.payments.payment_service_mocked_responses import perform_payment_refund, perform_payment_capture
from testing_utils.products.product_setup import ProductSetupInitializer

path_to_payment_service = 'services.payments.payment_service.PaymentService'
path_to_order_processing_replicator = 'replicators.order_processing_replicator.OrderProcessingReplicator'
# Path to the file with dramatiq actors which send emails related to different order actions
path_to_email_sending_tasks = 'apps.orders.tasks.email_sending'


Account = get_user_model()


class TestOrderCancellation(APITestCase):
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

    @mock.patch(path_to_email_sending_tasks + '.send_email_about_order_cancellation.send')
    @mock.patch(path_to_payment_service + '.perform_payment_refund')
    def test_pending_order_cancellation_should_be_succeeded(self, mocked_payment_refund: Mock,
                                                            mocked_email_sending: Mock):
        # Guarantee that products the user want to buy are sellable
        first_product = self.products[0]
        ProductSetupInitializer.update_product_availability(first_product, 11, True)
        second_product = self.products[1]
        ProductSetupInitializer.update_product_availability(second_product, 14, True)

        self._add_authorization_header()

        order_creation_response = self.order_testing_utils.create_unconfirmed_order(self.test_user,
                                                                     [first_product, second_product],
                                                                     self.addresses[0].original_id,
                                                                     )
        order_cancellation_response = self.order_testing_utils.send_request_to_cancel_order(
            order_creation_response.data["order_id"],
        )
        # Response should be HTTP 200
        self.assertEqual(order_cancellation_response.status_code, status.HTTP_200_OK)
        # Refund shouldn't be performed, because order is just pending and funds were not transferred.
        mocked_payment_refund.assert_not_called()
        # Email should be sent, since response is successful
        mocked_email_sending.assert_called()

    @mock.patch(path_to_email_sending_tasks + '.send_email_about_order_cancellation.send')
    @mock.patch(path_to_email_sending_tasks + '.send_email_with_order_confirmation.send')
    @mock.patch(path_to_payment_service + '.perform_payment_capture')
    @mock.patch(path_to_payment_service + '.perform_payment_refund')
    def test_processed_order_cancellation_should_be_succeeded(self,
                                                              mocked_payment_refund: Mock,
                                                              mocked_payment_capture: Mock,
                                                              mocked_send_order_confirmation_email: Mock,
                                                              mocked_send_order_cancellation_email: Mock,
                                                              ):
        """
        Processed order cancellation should be succeeded and refund must be performed.
        """
        mocked_payment_refund.side_effect = perform_payment_refund
        mocked_payment_capture.return_value = perform_payment_capture()

        # Guarantee that products the user want to buy are sellable
        first_product = self.products[0]
        ProductSetupInitializer.update_product_availability(first_product, 16, True)
        second_product = self.products[1]
        ProductSetupInitializer.update_product_availability(second_product, 19, True)

        self._add_authorization_header()

        order_creation_response = self.order_testing_utils.create_unconfirmed_order(self.test_user,
                                                                                    [first_product, second_product],
                                                                                    self.addresses[0].original_id,
                                                                                    )
        self.order_testing_utils.send_request_to_confirm_order(order_creation_response.data["order_id"],
                                                               order_creation_response.data["payment_id"],)
        mocked_payment_capture.assert_called()
        mocked_send_order_confirmation_email.assert_called()

        order_cancellation_response = self.order_testing_utils.send_request_to_cancel_order(
            order_creation_response.data["order_id"],
        )
        # Response should be HTTP 200
        self.assertEqual(order_cancellation_response.status_code, status.HTTP_200_OK)
        # Refund should be performed, because the order is already processed and funds were transferred.
        mocked_payment_refund.assert_called()
        # Email should be sent, since response is successful
        mocked_send_order_cancellation_email.assert_called()

    @mock.patch(path_to_email_sending_tasks + '.send_email_about_order_cancellation.send')
    @mock.patch(path_to_payment_service + '.perform_payment_refund')
    def test_already_canceled_order_cancellation_should_be_failed(self, mocked_payment_refund: Mock,
                                                            mocked_email_sending: Mock):
        # Guarantee that products the user want to buy are sellable
        first_product = self.products[0]
        ProductSetupInitializer.update_product_availability(first_product, 12, True)
        second_product = self.products[1]
        ProductSetupInitializer.update_product_availability(second_product, 11, True)

        self._add_authorization_header()

        order_creation_response = self.order_testing_utils.create_unconfirmed_order(self.test_user,
                                                                                    [first_product, second_product],
                                                                                    self.addresses[0].original_id,
                                                                                    )
        self.order_testing_utils.send_request_to_cancel_order(
            order_creation_response.data["order_id"],
        )

        another_cancellation_response =  self.order_testing_utils.send_request_to_cancel_order(
            order_creation_response.data["order_id"],
        )

        # The Response status code should be the same as in the OrderAlreadyCanceled API Exception
        self.assertEqual(another_cancellation_response.status_code, OrderAlreadyCanceled.status_code)
        # Refund shouldn't be performed, because the response is failed
        mocked_payment_refund.assert_not_called()
        # An Email about order cancellation should be sent only once,
        # because the order cancellation should be failed at the 2nd attempt.
        self.assertEqual(mocked_email_sending.call_count, 1)

    @mock.patch(path_to_email_sending_tasks + '.send_email_about_order_cancellation.send')
    @mock.patch(path_to_email_sending_tasks + '.send_email_with_order_confirmation.send')
    @mock.patch(path_to_payment_service + '.perform_payment_capture')
    @mock.patch(path_to_payment_service + '.perform_payment_refund')
    def test_completed_order_cancellation_should_be_failed(self,
                                                              mocked_payment_refund: Mock,
                                                              mocked_payment_capture: Mock,
                                                              mocked_send_order_confirmation_email: Mock,
                                                              mocked_send_order_cancellation_email: Mock,
                                                              ):
        """
        Returned or Delivered orders cannot be canceled.
        """
        mocked_payment_capture.return_value = perform_payment_capture()

        # Guarantee that products the user want to buy are sellable
        first_product = self.products[0]
        ProductSetupInitializer.update_product_availability(first_product, 13, True)
        second_product = self.products[1]
        ProductSetupInitializer.update_product_availability(second_product, 14, True)

        self._add_authorization_header()

        order_create_response = self.order_testing_utils.create_unconfirmed_order(self.test_user,
                                                                                    [first_product, second_product],
                                                                                    self.addresses[0].original_id,
                                                                                    )
        self.order_testing_utils.send_request_to_confirm_order(order_create_response.data["order_id"],
                                                               order_create_response.data["payment_id"], )
        mocked_payment_capture.assert_called()
        mocked_send_order_confirmation_email.assert_called()

        order = Order.objects.get(order_uuid=order_create_response.data["order_id"])
        # Simulate order shipment
        order.status = "shipped"
        order.save()
        # Simulate order delivery
        order.status = "delivered"
        order.save()

        order_cancellation_response = self.order_testing_utils.send_request_to_cancel_order(
            order_create_response.data["order_id"],
        )
        # The Response data and status should be as in the OrderIsCompleted API Exception
        self.assertEqual(order_cancellation_response.status_code, OrderIsCompleted.status_code)
        self.assertEqual(order_cancellation_response.data["detail"], OrderIsCompleted.default_detail)
        # Refund shouldn't be performed, because the response is failed
        mocked_payment_refund.assert_not_called()
        # Email shouldn't be sent, since response is BAD
        mocked_send_order_cancellation_email.assert_not_called()
