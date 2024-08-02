from django import forms
from django.core.exceptions import ValidationError

from .choices import RefundStatus
from .models import Refund

class RefundRequestAdminForm(forms.ModelForm):
    REQUEST_TYPE_CHOICES = [
        ('none', 'None'),  # Default option for no action
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    ]

    request_type = forms.ChoiceField(choices=REQUEST_TYPE_CHOICES, required=False, label='Request Type',)
    rejection_reason = forms.CharField(required=False, widget=forms.Textarea, label='Rejection Reason')

    class Meta:
        model = Refund
        fields = ['reason_for_return', 'order', 'status', 'approval_date', 'user',
                  'rejection_date', 'rejection_reason', 'request_type']

    def clean(self):
        cleaned_data = super().clean()
        request_type = cleaned_data.get('request_type')
        rejection_reason = cleaned_data.get('rejection_reason')
        status = self.instance.status

        if request_type == 'approve' and status != RefundStatus.PENDING:
            raise ValidationError("Only pending requests can be approved.")

        if request_type == 'reject':
            if status != RefundStatus.PENDING:
                raise ValidationError("Only pending requests can be rejected.")
            if not rejection_reason:
                raise ValidationError("Please provide a rejection reason when rejecting a request.")

        return cleaned_data