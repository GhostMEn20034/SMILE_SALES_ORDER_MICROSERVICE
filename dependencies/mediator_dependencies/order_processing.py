from typing import Optional

from dependencies.service_dependencies.addresses import get_address_service
from dependencies.service_dependencies.carts import get_cart_service
from dependencies.service_dependencies.orders import get_order_service
from dependencies.service_dependencies.payments import get_payment_service
from mediators.order_processing_coordinator import OrderProcessingCoordinator
from services.addresses.address_service import AddressService
from services.carts.cart_service import CartService
from services.orders.order_service import OrderService
from services.payments.payment_service import PaymentService
from mediators.service_list.order_processing_services import OrderProcessingServices


def get_order_processing_coordinator(order_service: Optional[OrderService] = None,
                                     payment_service: Optional[PaymentService] = None,
                                     address_service: Optional[AddressService] = None,
                                     cart_service: Optional[CartService] = None, ):
    if not order_service:
        order_service = get_order_service()

    if not payment_service:
        payment_service = get_payment_service()

    if not address_service:
        address_service = get_address_service()

    if not cart_service:
        cart_service = get_cart_service()

    services = OrderProcessingServices(
        order_service=order_service,
        payment_service=payment_service,
        address_service=address_service,
        cart_service=cart_service,
    )

    return OrderProcessingCoordinator(services)