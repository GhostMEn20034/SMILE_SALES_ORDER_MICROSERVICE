from mediators.service_list.order_processing_services import OrderProcessingServices
from param_classes.carts.cart_item_filters import CartItemFilters
from param_classes.order_processing_coordinator.order_creation import OrderCreationParams
from param_classes.orders.create_order import CreateOrderParams
from param_classes.payments.capture_payment_params import CapturePaymentParams
from param_classes.payments.initialize_payment import InitializePaymentParams
from result_classes.orders.create_order import CreateOrderResult
from result_classes.orders.order_creation_essentials import OrderCreationEssentialsParams


class OrderProcessingCoordinator:
    """
    Mediator class responsible for interactions related with order processing.
    """
    def __init__(self, services: OrderProcessingServices):
        self.services = services

    def create_order_and_initialize_payment(self, params: OrderCreationParams):
        cart_item_filters = CartItemFilters(cart_owner_id=params.cart_owner_id,
                                            product_ids=params.product_ids, include_only_saleable=True)
        cart_items = self.services.cart_service.get_cart_item_list(cart_item_filters)

        create_order_params = CreateOrderParams(
            user_id=params.cart_owner_id, address_id=params.address_id,
            product_ids=params.product_ids, cart_items=cart_items,
        )
        created_order: CreateOrderResult = self.services.order_service.create_order(create_order_params)
        create_payment_params = InitializePaymentParams(
            created_order,
        )

        # TODO: In the future, when there will be more than one payment provider,
        #  payment method resolver need to be written
        payment_data = self.services.payment_service.initialize_paypal_payment(create_payment_params)
        return payment_data

    def get_order_creation_essentials(self, user_id: int) -> OrderCreationEssentialsParams:
        """
        Returns all essential data to create a new order.
        """
        addresses = self.services.address_service.get_addresses(user_id)

        return OrderCreationEssentialsParams(
            addresses=addresses,
        )

    def complete_funds_transferring(self, data: CapturePaymentParams):
        """
        Captures the payment and updates the order status to "processed"
        """
        # TODO: In the future, when there will be more than one payment provider,
        #  payment method resolver need to be written
        capture_success_data = self.services.payment_service.perform_paypal_payment_capture(data)
        return capture_success_data
