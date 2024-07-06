from typing import List, Optional, Dict
from django.db.models import QuerySet

from apps.carts.models import CartItem, Cart
from apps.carts.serializers.api_serializers import CartItemWithProductSerializer
from param_classes.carts.cart_item_filters import CartItemFilters


class CartService:
    def __init__(self, cart_queryset: QuerySet[Cart], cart_item_queryset: QuerySet[CartItem]):
        self.cart_queryset = cart_queryset
        self.cart_item_queryset = cart_item_queryset

    def get_cart_item_list(self, params: CartItemFilters) -> QuerySet[CartItem]:
        filters = {
            "cart__user_id": params.cart_owner_id
        }
        if params.product_ids is not None:
            filters['product_id__in'] = params.product_ids

        if params.include_only_saleable:
            filters['product__for_sale'] = True
            filters['product__stock__gt'] = 0

        cart_items = self.cart_item_queryset.filter(**filters).select_related('product') \
            .only('quantity', 'product__max_order_qty', 'product__stock',
                  'product__object_id', 'product__name', 'product__tax_rate',
                  'product__price', 'product__discount_rate', 'product__image', 'product__for_sale')

        return cart_items

    def get_cart_items(self, cart_owner_id: int, product_ids: Optional[List[str]]) -> List[Dict]:
        cart_item_filters = CartItemFilters(cart_owner_id=cart_owner_id, product_ids=product_ids)
        cart_items = self.get_cart_item_list(cart_item_filters)
        cart_item_serializer = CartItemWithProductSerializer(instance=cart_items, many=True)
        return cart_item_serializer.data
