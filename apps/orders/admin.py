from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ('order_uuid', )
    list_filter = ('is_abandoned', )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        return OrderItem.objects.all().select_related('order')

    fields = ('order', 'product', 'price_per_unit', 'quantity', 'amount')
    list_display = ('order', 'product', 'price_per_unit', 'quantity', )
    readonly_fields = ('amount', )
    search_fields = ('order__order_uuid', )