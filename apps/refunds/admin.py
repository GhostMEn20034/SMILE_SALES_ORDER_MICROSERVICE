from django.contrib import admin
from django.db.models import Prefetch
from django.contrib import messages

from .forms import RefundRequestAdminForm
from .models import Refund
from .admin_exceptions import RefundApprovalFailedException, RefundRejectionFailedException
from apps.payments.models import Payment
from dependencies.mediator_dependencies.order_processing import get_order_processing_coordinator



@admin.register(Refund)
class RefundRequestAdmin(admin.ModelAdmin):
    form = RefundRequestAdminForm
    list_display = ('order', 'reason_for_return', 'status', 'approval_date', 'rejection_date', 'user', )
    list_filter = ('status',)
    readonly_fields = ('status', 'approval_date', 'rejection_date', )

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.order_processing_coordinator = get_order_processing_coordinator()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('order').prefetch_related(
            Prefetch('order__payments', queryset=Payment.objects.filter(type="payment"))
        )
        return queryset

    def save_model(self, request, obj, form, change):
        request_type = form.cleaned_data.get('request_type')

        if request_type == 'approve':
            try:
                self.order_processing_coordinator.approve_refund_request(obj)
                self.message_user(request, "Refund approved successfully!", messages.SUCCESS)
            except RefundApprovalFailedException as e:
                self.message_user(request, str(e), messages.ERROR)

        elif request_type == 'reject':
            rejection_reason = form.cleaned_data.get('rejection_reason')
            try:
                self.order_processing_coordinator.reject_refund_request(obj, rejection_reason)
                self.message_user(request, "Refund rejected successfully!", messages.SUCCESS)
            except RefundRejectionFailedException as e:
                self.message_user(request, str(e), messages.ERROR)
        else:
            super().save_model(request, obj, form, change)
