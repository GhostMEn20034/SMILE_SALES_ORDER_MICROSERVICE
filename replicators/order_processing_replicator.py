from typing import Iterable
from django.conf import settings

from apps.orders.models import OrderItem
from apps.core.tasks import perform_data_topic_replication


class OrderProcessingReplicator:
    """
    A class to handle the replication of order processing tasks such as reserving and releasing products.
    """
    def __init__(self):
        self.base_routing_key_name = 'orders'
        self.exchange_name = settings.ORDER_PROCESSING_EXCHANGE_TOPIC_NAME

    def reserve_products_and_remove_cart_items(self, user_id: int, order_items: Iterable[OrderItem]):
        """
        Prepares and sends data for reserving products and cart items removal as part of the replication process.
        Note that order_item's product_id is also used for cart_items removal.
        :param order_items: An iterable of the order's products to be reserved.
        :param user_id: The user that owns cart_items.
        """
        data = {}
        products = []
        for order_item in order_items:
            products.append({
                'product_id': order_item.product_id,
                'quantity': order_item.quantity,
            })

        data['products'] = products
        data['user_id'] = user_id

        routing_key = self.base_routing_key_name + '.products.reserve_and_remove_cart_items'
        perform_data_topic_replication.send(self.exchange_name, routing_key, data)

    def release_products(self, order_items: Iterable[OrderItem]):
        """
        Prepares and sends data for releasing products as part of the replication process.
        :param order_items:An iterable of the order's products to be released.
        """
        data = {}
        products = []

        for order_item in order_items:
            products.append({
                'product_id': order_item.product_id,
                'quantity': order_item.quantity,
            })
        data['products'] = products

        routing_key = self.base_routing_key_name + '.products.release'
        perform_data_topic_replication.send(self.exchange_name, routing_key, data)
