import uuid

from apps.orders.models import Order
from apps.payments.exceptions import PaymentCaptureFailedException
from apps.payments.models import Payment
from mediators.service_list.order_processing_services import OrderProcessingServices
from param_classes.carts.cart_item_filters import CartItemFilters
from param_classes.order_processing_coordinator.order_cancelation import OrderCancellationParams
from param_classes.order_processing_coordinator.order_creation import OrderCreationParams
from param_classes.orders.create_order import CreateOrderParams
from param_classes.payments.capture_payment_params import CapturePaymentParams
from param_classes.payments.initialize_payment import InitializePaymentParams
from param_classes.payments.payment_creation import PaymentCreationParams
from result_classes.order_processing_coordinator.order_details import OrderDetailsResult
from result_classes.orders.create_order import CreateOrderResult
from result_classes.orders.order_creation_essentials import OrderCreationEssentialsParams
from apps.orders.exceptions import OrderDoesNotExist


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


    def complete_funds_transferring(self, data: CapturePaymentParams) -> Payment:
        """
        Captures the payment and updates the order status to "processed"
        """
        # TODO: In the future, when there will be more than one payment provider,
        #  payment method resolver need to be written
        capture_success_data = self.services.payment_service.perform_paypal_payment_capture(data)

        try:
            modified_order = self.services.order_service.process_order(data.order_id)
        except Order.DoesNotExist:
            raise OrderDoesNotExist

        capture = capture_success_data.captures[0]
        payment_creation_params = PaymentCreationParams(
            payment_id=capture_success_data.payment_id,
            capture=capture,
            user_id=data.user_id,
            order_id=modified_order.order_uuid,
            provider=data.provider,
            status="success",
        )
        created_payment = self.services.payment_service.create_payment(payment_creation_params)
        if created_payment is None:
            raise PaymentCaptureFailedException

        return created_payment

    def cancel_order(self, params: OrderCancellationParams) -> Order:
        """
        Cancels the order and updates the order status to "canceled"
        """
        try:
            order = self.services.order_service.cancel_order(params.order_uuid)
        except Order.DoesNotExist:
            raise OrderDoesNotExist

        return order
