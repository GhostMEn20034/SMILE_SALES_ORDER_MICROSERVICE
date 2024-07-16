from rest_framework.serializers import ModelSerializer
from apps.products.models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'