from datetime import timedelta
import dramatiq
from dramatiq_crontab import cron
from django.conf import settings
from django.utils import timezone

from apps.orders.models import Order
from dependencies.service_dependencies.products import get_product_service
from replicators.order_processing_replicator import OrderProcessingReplicator


@cron(f"*/{settings.CHECK_ABANDONED_ORDERS_EVERY_MINUTES} * * * *")  # Run task every N minutes
@dramatiq.actor
def release_products_from_abandoned_orders():
    release_products_from_abandoned_orders.logger.info("Searching for abandoned orders...")
    # Calculate the time threshold (current time minus 45 minutes)
    time_threshold = timezone.now() - timedelta(minutes=45)
    abandoned_orders = Order.objects.filter(is_abandoned=True, created_at__lt=time_threshold) \
        .prefetch_related('order_items')

    product_service = get_product_service()
    order_processing_replicator = OrderProcessingReplicator()

    # list with all order items collected from the orders
    all_order_items = []

    # Append all order items to the one array
    for order in abandoned_orders:
        order_items = order.order_items.all()
        for order_item in order_items:
            all_order_items.append(order_item)

    if all_order_items:
        # Release products which appear in order items in order microservice
        product_service.release_from_order(all_order_items)
        # Send message to release products which appear in order items in other microservices
        order_processing_replicator.release_products(all_order_items)
        # Delete all matched abandoned orders
        abandoned_orders.delete()

        order_ids = [order.order_uuid for order in abandoned_orders]
        release_products_from_abandoned_orders.logger.info(
            f"Products released from the abandoned orders: {','.join(order_ids)}"
        )
