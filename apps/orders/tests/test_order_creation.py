from typing import List

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from unittest import mock

from apps.addresses.models import Address
from apps.orders.models import OrderItem
from apps.products.models import Product
from testing_utils.orders.order_utils import OrderTestingUtils
from testing_utils.payments.payment_service_mocked_responses import initialize_payment
from testing_utils.products.product_setup import ProductSetupInitializer
from testing_utils.carts.cart_setup import CartSetupInitializer
from testing_utils.common.test_case_setup import setup_order_api_test_case
from apps.carts.exceptions import NoSellableCartItems


path_to_payment_service = 'services.payments.payment_service.PaymentService'
path_to_order_processing_replicator = 'replicators.order_processing_replicator.OrderProcessingReplicator'


Account = get_user_model()


class TestOrderCreation(APITestCase):
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

    def _send_request_to_create_order(self, product_ids: List[str]):
        """
        Sends a request to create an order.
        :param product_ids: List of product IDs for the order
        """
        return self.order_testing_utils.send_request_to_create_order(
            product_ids,
            self.addresses[0].original_id,
        )


    @mock.patch(path_to_order_processing_replicator + '.reserve_products_and_remove_cart_items')
    def test_order_creation_with_correct_data_must_be_successful(self, mocked_product_reservation):
        """
        If all data is correct, all products the user want to buy are sellable, then response should be successful.
        """
        # Guarantee that products the user want to buy are sellable
        first_product = self.products[0]
        ProductSetupInitializer.update_product_availability(first_product, 10, True)

        second_product = self.products[1]
        ProductSetupInitializer.update_product_availability(second_product, 15, True)

        # Create a list with product the user want to buy
        product_ids = [
            first_product.object_id,
            second_product.object_id,
        ]

        # Create cart items
        cart_setup = CartSetupInitializer()
        cart = cart_setup.create_cart(self.test_user)
        cart_setup.add_products_to_cart(cart, product_ids, 2)

        # Set the authorization header with the token
        self._add_authorization_header()

        with mock.patch(path_to_payment_service + ".initialize_payment") as mocked_payment_initialization:
            mocked_payment_initialization.return_value = initialize_payment()
            response = self._send_request_to_create_order(product_ids)

        # Request must have HTTP 201 Status, since the input data from the request body is correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that payment_id, checkout_link and order_id are in response data
        self.assertIn("payment_id", response.data)
        self.assertIn("checkout_link", response.data)
        self.assertIn("order_id", response.data)

        # product reservation must be called once because the response status is successful.
        self.assertEqual(mocked_product_reservation.call_count, 1)

    @mock.patch(path_to_order_processing_replicator + '.reserve_products_and_remove_cart_items')
    def test_should_create_order_only_with_sellable_products(self, mocked_product_reservation):
        """
        If the user wants to create an order with products where Product1 is sellable and Product2 is not,
        then the order will have only an order item related to Product1.
        """

        # Guarantee that product1 is sellable, and product2 is not
        first_product = self.products[0]
        ProductSetupInitializer.update_product_availability(first_product, 10, True)

        second_product = self.products[1]
        ProductSetupInitializer.update_product_availability(second_product, 1, False)

        # Create a list with product the user want to buy
        product_ids = [
            first_product.object_id,
            second_product.object_id,
        ]

        # Create cart items
        cart_setup = CartSetupInitializer()
        cart = cart_setup.create_cart(self.test_user)
        cart_setup.add_products_to_cart(cart, product_ids, 2)

        # Set the authorization header with the token
        self._add_authorization_header()

        with mock.patch(path_to_payment_service + ".initialize_payment") as mocked_payment_initialization:
            mocked_payment_initialization.return_value = initialize_payment()
            response = self._send_request_to_create_order(product_ids)

        # Request must have HTTP 201 Status, since the input data from the request body is correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Find the order items with returned order_id
        order_items_count = OrderItem.objects.filter(order_id=response.data['order_id']).count()
        self.assertEqual(order_items_count, 1)
        # product reservation must be called once because the response status is successful.
        self.assertEqual(mocked_product_reservation.call_count, 1)

    @mock.patch(path_to_order_processing_replicator + '.reserve_products_and_remove_cart_items')
    @mock.patch(path_to_payment_service + '.initialize_payment', )
    def test_create_order_with_unsellable_products_should_fail(self, _, mocked_product_reservation):
        """
        The user cannot create an order with unsellable products.
        """
        # Make first 2 products unsellable
        first_product = self.products[0]
        ProductSetupInitializer.update_product_availability(first_product, 10, False)

        second_product = self.products[1]
        ProductSetupInitializer.update_product_availability(second_product, 0, False)

        product_ids = [
            first_product.object_id,
            second_product.object_id
        ]

        # Create cart items
        cart_setup = CartSetupInitializer()
        cart = cart_setup.create_cart(self.test_user)
        cart_setup.add_products_to_cart(cart, product_ids, 2)

        # Set the authorization header with the token
        self._add_authorization_header()

        response = self._send_request_to_create_order(product_ids)

        # Request must have HTTP 400 Status since the user sent only unsellable products
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], NoSellableCartItems.default_detail)

        # product reservation must not be called since NoSellableCartItems was raised before the product reservation
        self.assertEqual(mocked_product_reservation.call_count, 0)
