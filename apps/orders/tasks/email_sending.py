import uuid
from typing import List, Dict

import dramatiq
from django.db.models import Prefetch, Sum, F
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail

from apps.orders.models import Order, OrderItem
from apps.payments.models import Payment


def _send_email(template_name: str, template_context: Dict, receivers: List[str]):
    convert_to_html_content = render_to_string(
        template_name=template_name,
        context=template_context
    )

    plain_message = strip_tags(convert_to_html_content)

    send_mail(
        subject="Your Smile Sales Order",
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=receivers,
        html_message=convert_to_html_content,
        fail_silently=True,
    )

@dramatiq.actor
def send_email_with_order_confirmation(user_id: int, order_id: uuid.UUID, provider_payment_id: str):
    order: Order = Order.objects.select_related('address').select_related('user').prefetch_related(
        Prefetch('order_items', queryset=OrderItem.objects.select_related('product'))
    ).annotate(
        total_amount_before_tax=Sum(F('order_items__amount')),
        total_tax=Sum(F('order_items__tax_per_unit') * F('order_items__quantity')),
    ).get(user_id=user_id, order_uuid=order_id)

    try:
        payment = Payment.objects.get(provider_payment_id=provider_payment_id)
    except Payment.DoesNotExist:
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
        receivers=[order.user.email, ]
    )


