from rest_framework import serializers

from apps.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductPublicDataSerializer(serializers.ModelSerializer):
    discounted_price = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Product
        exclude = ('parent_id', 'tax_rate', 'sku', 'event_id', )