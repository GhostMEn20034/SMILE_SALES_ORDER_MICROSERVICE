from services.addresses.address_service import AddressService
from services.carts.cart_service import CartService
from services.orders.order_service import OrderService
from services.payments.payment_service import PaymentService
from services.products.product_service import ProductService
from services.refunds.refund_service import RefundService


class OrderProcessingServices:
    """
    Encapsulates all services for Order Processing Coordinator
    """
    def __init__(self, order_service: OrderService, payment_service: PaymentService, cart_service: CartService,
                 address_service: AddressService, product_service: ProductService, refund_service: RefundService):
        self.order_service = order_service
        self.payment_service = payment_service
        self.cart_service = cart_service
        self.address_service = address_service
        self.product_service = product_service
        self.refund_service = refund_service
