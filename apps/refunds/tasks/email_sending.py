import dramatiq
from django.conf import settings

from apps.payments.models import Payment
from apps.refunds.models import Refund
from utils.core.email_utils import send_email


@dramatiq.actor
def send_email_about_refund_rejection(refund_id: int):
    try:
        refund = Refund.objects.select_related('user').get(id=refund_id)
    except Refund.DoesNotExist:
        send_email_about_refund_rejection.logger.error("Wrong Refund ID was passed")
        return None

    template_context = {
        'refund': refund,
        'frontend_url': settings.FRONTEND_BASE_URL,
    }

    send_email(
        template_name='refunds/refund_rejected/main.html',
        template_context=template_context,
        receivers=[refund.user.email, ],
        subject=f'Refund Request Denied - Order #{refund.order_id}',
    )
    send_email_about_refund_rejection.logger.info("An email about refund rejection has been sent!")

@dramatiq.actor
def send_email_about_refund_approval(refund_id: int, payment_id: int):
    try:
        refund = Refund.objects.select_related('user').get(id=refund_id)
        payment = Payment.objects.get(id=payment_id)
    except Refund.DoesNotExist:
        send_email_about_refund_rejection.logger.error(f"The Refund with ID {refund_id} does not exist")
        return None
    except Payment.DoesNotExist:
        send_email_about_refund_approval.logger.error(f"The Payment with ID {payment_id} does not exist")
        return None
    except Exception as e:
        send_email_about_refund_approval.logger.error(f"An unexpected error occurred: {e}")
        return None

    template_context = {
        'refund': refund,
        'payment': payment,
        'frontend_url': settings.FRONTEND_BASE_URL,
    }

    send_email(
        template_name='refunds/refund_approved/main.html',
        template_context=template_context,
        receivers=[refund.user.email, ],
        subject=f'Refund Request Approved - Order #{refund.order_id}'
    )
