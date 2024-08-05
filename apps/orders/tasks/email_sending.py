import uuid
from typing import List, Dict, Optional

import dramatiq
from django.contrib.auth import get_user_model
from django.db.models import Prefetch, Sum, F
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail

from apps.orders.models import Order, OrderItem
from apps.payments.models import Payment

User = get_user_model()

def _send_email(template_name: str, template_context: Dict, receivers: List[str], subject: str):
    convert_to_html_content = render_to_string(
        template_name=template_name,
        context=template_context
    )

    plain_message = strip_tags(convert_to_html_content)

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=receivers,
        html_message=convert_to_html_content,
        fail_silently=True,
    )

@dramatiq.actor
def send_email_with_order_confirmation(user_id: int, order_id: uuid.UUID, provider_payment_id: str):
    try:
        order: Order = Order.objects.select_related('address').select_related('user').prefetch_related(
            Prefetch('order_items', queryset=OrderItem.objects.select_related('product'))
        ).annotate(
            total_amount_before_tax=Sum(F('order_items__amount')),
            total_tax=Sum(F('order_items__tax_per_unit') * F('order_items__quantity')),
        ).get(user_id=user_id, order_uuid=order_id)
        send_email_with_order_confirmation.logger.info("Order is found")
    except Order.DoesNotExist as e:
        send_email_with_order_confirmation.logger.error("Wrong User ID and Order ID were passed")
        raise e

    try:
        payment = Payment.objects.get(provider_payment_id=provider_payment_id)
    except Payment.DoesNotExist:
        send_email_with_order_confirmation.logger.error("Wrong Payment ID was passed")
        payment = {}

    template_context = {
        'order': order,
        'payment': payment,
        'address': order.address,
        'frontend_url': settings.FRONTEND_BASE_URL,
        'order_total': round(order.total_amount_before_tax + order.total_tax, 2),
    }

    _send_email(
        template_name='orders/order_confirmed/main.html',
        template_context=template_context,
        receivers=[order.user.email, ],
        subject="Your Smile Sales Order",
    )
    send_email_with_order_confirmation.logger.info("An Email about Order placement has been sent")

@dramatiq.actor
def send_email_about_order_cancellation(user_id: int, order_id: uuid.UUID, provider_payment_id: Optional[str] = None):
    try:
        user: User = User.objects.get(original_id=user_id)
    except User.DoesNotExist:
        send_email_about_order_cancellation.logger.error("Wrong User ID was passed")
        return None

    template_context = {
        'user': user,
        'order_id': order_id,
        'payment_id': provider_payment_id,
        'frontend_url': settings.FRONTEND_BASE_URL,
    }

    _send_email(
        'orders/order_canceled/main.html',
        template_context=template_context,
        receivers=[user.email, ],
        subject="Smile Sales Order Cancellation",
    )
    send_email_about_order_cancellation.logger.info("An Email about order cancellation has been sent!")
