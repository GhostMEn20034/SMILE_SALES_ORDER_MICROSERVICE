from rest_framework import serializers


class OrderCreationRequestBody(serializers.Serializer):
    cart_owner_id = serializers.IntegerField(min_value=1)
    address_id = serializers.IntegerField(min_value=1)
    product_ids = serializers.ListField(child=serializers.CharField(), required=False)


class OrderListFiltersRequestBody(serializers.Serializer):
    ORDER_STATUS_CHOICES = ["allOrders", "notShipped", "canceledOrders"]

    order_status = serializers.ChoiceField(choices=ORDER_STATUS_CHOICES)
    time_filter = serializers.CharField(required=False, allow_null=True)


class ChangeArchivedStatusRequestBody(serializers.Serializer):
    PURPOSE_CHOICES = ['archive', 'unarchive']

    purpose = serializers.ChoiceField(choices=PURPOSE_CHOICES)
