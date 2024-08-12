import uuid
from typing import List
from unittest import mock

from django.contrib.auth import get_user_model
from django.db import transaction
from django.test.client import Client
from django.urls import reverse

from apps.orders.models import Order, OrderItem
from apps.payments.models import Payment
from apps.products.models import Product
from testing_utils.carts.cart_setup import CartSetupInitializer
from testing_utils.payments.payment_service_mocked_responses import initialize_payment


path_to_payment_service = 'services.payments.payment_service.PaymentService'


Account = get_user_model()


class OrderTestingUtils:
    create_order_link = reverse('orders-list')

    def __init__(self, client: Client):
        self.client = client

    @staticmethod
    def get_order_confirmation_link(payment_id: str) -> str:
        paypal_payment_url = reverse(
            'paypal-payment-perform-capture',
            kwargs={'payment_id': payment_id}
        )
        return paypal_payment_url

    def send_request_to_confirm_order(self, order_id: uuid.UUID, payment_id: str):
        return self.client.post(
            self.get_order_confirmation_link(payment_id),
            data={"order_id": order_id},
            format='json',
        )

    def send_request_to_create_order(self, product_ids: List[str], address_id: int):
        """
        Sends a request to create an order.
        :param product_ids: List of product IDs for the order
        :param address_id: ID of the address where the order must be delivered
        """
        return self.client.post(self.create_order_link,
                                data={
                                    'address_id': address_id,
                                    'product_ids': product_ids,
                                },
                                format='json',
                                )

    def send_request_to_cancel_order(self, order_id: uuid.UUID):
        """
        Sends a request to cancel the order.
        :param order_id: Order identifier
        """
        cancel_order_link = reverse('orders-cancel-order', kwargs={"order_uuid": order_id})
        return self.client.post(cancel_order_link)


    def send_request_to_archive_order(self, order_id: uuid.UUID, purpose: str = "archive"):
        """
        Sends a request to archive the order.
        :param order_id: Order identifier
        :param purpose: Specify "archive" if you want to archive the order,
        and specify "unarchive" to unarchive the order
        """
        cancel_order_link = reverse('orders-archive-order', kwargs={"order_uuid": order_id})
        return self.client.put(cancel_order_link, data={'purpose': purpose}, format='json')

    def create_unconfirmed_order(self, account: Account, products: List[Product], address_id: int):
        # Create a list with product the user want to buy
        product_ids = [product.object_id for product in products]

        # Create cart items
        cart_setup = CartSetupInitializer()
        cart = cart_setup.create_cart(account)
        cart_setup.add_products_to_cart(cart, product_ids, 2)

        with mock.patch(path_to_payment_service + ".initialize_payment") as mocked_payment_initialization:
            mocked_payment_initialization.return_value = initialize_payment()
            response = self.send_request_to_create_order(product_ids, address_id)
            return response

    @staticmethod
    def create_test_order(account: Account, products: List[Product], address_id: int) -> Order:
        with transaction.atomic():
            order = Order.objects.create(
                user=account,
                address_id=address_id,
                is_abandoned=False,
                status="processed",
            )

            order_items = []
            for product in products:
                order_item = OrderItem(
                    order=order,
                    product=product,
                    price_per_unit=product.price,
                    tax_rate=product.tax_rate,
                    quantity=1,
                )
                order_items.append(order_item)

            order_items: List[OrderItem] = OrderItem.objects.bulk_create(order_items)

            order_total = 0
            for order_item in order_items:
                order_total += order_item.amount_with_tax

            Payment.objects.create(
                user=account,
                order=order,
                net_amount=round(order_total, 2),
                status="success",
                provider_payment_id="5O190127TN364715T",
                capture_id="3C679366HH908993F",
                provider="paypal",
            )

            return order