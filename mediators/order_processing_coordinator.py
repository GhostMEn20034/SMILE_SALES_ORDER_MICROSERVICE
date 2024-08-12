import logging
from typing import Optional, Tuple
from django.db import transaction
from django.utils import timezone

from apps.carts.exceptions import NoSellableCartItems
from apps.orders.models import Order
from apps.payments.exceptions import (
    PaymentCaptureFailedException, PaymentCreationFailedException,
    PaymentToRefundNotFoundException, PaymentRefundFailedException
)
from apps.payments.models import Payment
from apps.refunds.admin_exceptions import RefundApprovalFailedException
from apps.refunds.models import Refund
from mediators.service_list.order_processing_services import OrderProcessingServices
from param_classes.carts.cart_item_filters import CartItemFilters
from param_classes.order_processing_coordinator.order_cancelation import OrderCancellationParams
from param_classes.order_processing_coordinator.order_creation import OrderCreationParams
from param_classes.order_processing_coordinator.refund_payment_approval import RefundPaymentApprovalParams
from param_classes.orders.create_order import CreateOrderParams
from param_classes.payments.capture_payment_params import CapturePaymentParams
from param_classes.payments.initialize_payment import InitializePaymentParams
from param_classes.payments.payment_creation import PaymentCreationParams
from param_classes.payments.refund_creation import RefundCreationParams
from param_classes.refunds.refund_request_creation import RefundRequestCreationParams
from result_classes.orders.create_order import CreateOrderResult
from result_classes.orders.order_cancellation import OrderCancellationResult
from result_classes.orders.order_creation_essentials import OrderCreationEssentialsParams
from replicators.order_processing_replicator import OrderProcessingReplicator
from apps.orders.exceptions import OrderDoesNotExist, DeliveredOrdersOnlyEligibleForRefundException
from services.payments.payment_responses.paypal.create_payment_response import CreatePaypalPaymentResponse


class OrderProcessingCoordinator:
    """
    Mediator class responsible for interactions related with order processing.
    """

    def __init__(self, services: OrderProcessingServices, order_processing_replicator: OrderProcessingReplicator):
        self.services = services
        self.order_processing_replicator = order_processing_replicator

    def create_order_and_initialize_payment(self, params: OrderCreationParams) \
            -> Tuple[CreateOrderResult, CreatePaypalPaymentResponse]:
        cart_item_filters = CartItemFilters(cart_owner_id=params.cart_owner_id,
                                            product_ids=params.product_ids, include_only_saleable=True)
        cart_items = self.services.cart_service.get_cart_item_list(cart_item_filters)
        if cart_items.count() == 0:
            raise NoSellableCartItems

        create_order_params = CreateOrderParams(
            user_id=params.cart_owner_id, address_id=params.address_id,
            product_ids=params.product_ids, cart_items=cart_items,
        )
        try:
            with transaction.atomic():
                created_order: CreateOrderResult = self.services.order_service.create_order(create_order_params)
                create_payment_params = InitializePaymentParams(
                    created_order,
                )
                # TODO: In the future, when there will be more than one payment provider,
                #  payment method resolver need to be written
                payment_data = self.services.payment_service.initialize_payment(create_payment_params)
        except PaymentCreationFailedException as e:
            logging.error(f"{str(timezone.now())}{e.default_detail}")
            raise e
        else:
            order_items = created_order.order_items
            with transaction.atomic():
                self.services.cart_service.delete_cart_items_by_queryset(cart_items)
                self.services.product_service.reserve_for_order(order_items)
                self.order_processing_replicator.reserve_products_and_remove_cart_items(params.cart_owner_id,
                                                                                        order_items)

        return created_order, payment_data

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
        with transaction.atomic():
            try:
                modified_order = self.services.order_service.process_order(data.order_id, data.user_id)
            except Order.DoesNotExist:
                raise OrderDoesNotExist

            # TODO: In the future, when there will be more than one payment provider,
            #  payment method resolver need to be written
            capture_success_data = self.services.payment_service.perform_payment_capture(data)

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

            self.services.order_service.send_order_confirmation_email(data.user_id, data.order_id, created_payment)
            return created_payment

    def _refund_payment_on_cancel(self, order: Order) -> Payment:
        """
        Attempts to refund the payment for the given order.
        Raises PaymentToRefundNotFoundException if the payment record related with the passed order is not found.
        Raises PaymentRefundFailedException if refund failed.
        """
        try:
            payment = order.payments.get(type="payment")
        except Payment.DoesNotExist:
            raise PaymentToRefundNotFoundException

        refund_response = self.services.payment_service.perform_payment_refund(
            payment, "Order cancelling",
        )
        create_refund_params = RefundCreationParams(
            refund_id=refund_response.refund_id,
            user_id=int(order.user_id),
            order_id=order.order_uuid,
            provider=payment.provider,
            status="success",
            refund_breakdown=refund_response.refund_breakdown,
        )
        created_refund = self.services.payment_service.create_refund(create_refund_params)

        if created_refund is None:
            raise PaymentRefundFailedException

        return created_refund

    def cancel_order(self, params: OrderCancellationParams) -> OrderCancellationResult:
        """
        Cancels the order and updates the order status to "canceled".
        Potential errors:
            - If the order is not found, OrderDoesNotExist exception will be raised.
            - If the order is already canceled, OrderAlreadyCanceled exception will be raised.
            - if the order is already finalized, OrderIsFinalized exception will be raised.
            - Other potential errors you can find in self._refund_payment_on_cancel
        Raises PaymentRefundFailedException if refund failed.
        """
        with transaction.atomic():
            try:
                order_after_update, order_before_update = self.services.order_service.cancel_order(
                    params.order_uuid, params.user_id
                )
            except Order.DoesNotExist:
                raise OrderDoesNotExist

            order_items = order_after_update.order_items.all()

            payment = None
            if order_before_update.is_processed():
                payment = self._refund_payment_on_cancel(order_after_update)

            self.services.product_service.release_from_order(order_items)
            self.order_processing_replicator.release_products(order_items)
            self.services.order_service.send_order_cancellation_email(
                params.user_id, order_after_update.order_uuid, payment
            )

            return OrderCancellationResult(
                order=order_after_update,
                payment=payment,
            )

    def create_refund_request(self, params: RefundRequestCreationParams) -> Refund:
        try:
            order = self.services.order_service.get_by_uuid_if_owner(
                user_id=params.user_id,
                order_uuid=params.order_id,
            )
        except Order.DoesNotExist:
            raise OrderDoesNotExist

        if not order.is_delivered():
            raise DeliveredOrdersOnlyEligibleForRefundException

        refund = self.services.refund_service.create_refund(params)
        return refund

    def _refund_payment_on_refund_approval(self, params: RefundPaymentApprovalParams) -> Optional[Payment]:
        refund_response = self.services.payment_service.perform_payment_refund(
            params.payment, params.refund_reason
        )
        create_refund_params = RefundCreationParams(
            refund_id=refund_response.refund_id,
            user_id=int(params.user_id),
            order_id=params.order_id,
            provider=params.payment.provider,
            status="success",
            refund_breakdown=refund_response.refund_breakdown,
        )
        created_refund = self.services.payment_service.create_refund(create_refund_params)

        return created_refund

    def approve_refund_request(self, refund: Refund) -> None:
        with transaction.atomic():
            try:
                # Find a payment with payment type "payment" or you can call it "Regular payment"
                payment = refund.order.payments.get(type="payment")
            except Payment.DoesNotExist:
                raise RefundApprovalFailedException("There's no payment for this order")

            order = refund.order

            refund_payment_approval_params = RefundPaymentApprovalParams(
                payment=payment,
                refund_reason=refund.get_reason_for_return_display(),
                order_id=order.order_uuid,
                user_id=int(order.user_id),
            )
            try:
                # Create a payment with payment type "refund"
                created_refund = self._refund_payment_on_refund_approval(refund_payment_approval_params)
            except PaymentRefundFailedException:
                raise RefundApprovalFailedException("Payment refund failed")

            # If the payment refund is None, it means that it's not created due to payment's invalid data
            if created_refund is None:
                raise RefundApprovalFailedException("Payment is not created")

            self.services.order_service.mark_as_returned(order)
            self.services.refund_service.approve_refund(refund)
            self.services.refund_service.send_refund_request_approval_email(refund, created_refund)

    def reject_refund_request(self, refund: Refund, rejection_reason: str) -> None:
        with transaction.atomic():
            self.services.refund_service.reject_refund(refund, rejection_reason)
            self.services.refund_service.send_refund_request_rejection_email(refund)
