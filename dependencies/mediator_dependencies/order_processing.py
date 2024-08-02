from typing import Optional

from dependencies.service_dependencies.addresses import get_address_service
from dependencies.service_dependencies.carts import get_cart_service
from dependencies.service_dependencies.orders import get_order_service
from dependencies.service_dependencies.payments import get_payment_service
from dependencies.service_dependencies.products import get_product_service
from dependencies.service_dependencies.refunds import get_refund_service
from mediators.order_processing_coordinator import OrderProcessingCoordinator
from services.addresses.address_service import AddressService
from services.carts.cart_service import CartService
from services.orders.order_service import OrderService
from services.payments.payment_service import PaymentService
from mediators.service_list.order_processing_services import OrderProcessingServices
from replicators.order_processing_replicator import OrderProcessingReplicator
from services.products.product_service import ProductService
from services.refunds.refund_service import RefundService


def get_order_processing_coordinator(order_service: Optional[OrderService] = None,
                                     payment_service: Optional[PaymentService] = None,
                                     address_service: Optional[AddressService] = None,
                                     cart_service: Optional[CartService] = None,
                                     product_service: Optional[ProductService] = None,
                                     refund_service: Optional[RefundService] = None,
                                     ):
    if not order_service:
        order_service = get_order_service()

    if not payment_service:
        payment_service = get_payment_service()

    if not address_service:
        address_service = get_address_service()

    if not cart_service:
        cart_service = get_cart_service()

    if not product_service:
        product_service = get_product_service()

    if not refund_service:
        refund_service = get_refund_service()

    services = OrderProcessingServices(
        order_service=order_service,
        payment_service=payment_service,
        address_service=address_service,
        cart_service=cart_service,
        product_service=product_service,
        refund_service=refund_service,
    )

    order_processing_replicator = OrderProcessingReplicator()

    return OrderProcessingCoordinator(services, order_processing_replicator)
