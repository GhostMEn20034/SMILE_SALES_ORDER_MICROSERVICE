from typing import Dict, List

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email(template_name: str, template_context: Dict, receivers: List[str], subject: str):
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
