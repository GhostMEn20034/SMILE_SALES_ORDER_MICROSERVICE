from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    fields = ('order', 'product', 'price_per_unit', 'quantity', 'amount')
    list_display = ('order', 'product', 'price_per_unit', 'quantity', )
    readonly_fields = ('amount', )