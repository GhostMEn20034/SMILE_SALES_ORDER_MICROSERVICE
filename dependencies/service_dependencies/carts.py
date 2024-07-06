from apps.carts.models import Cart, CartItem
from services.carts.cart_service import CartService


def get_cart_service() -> CartService:
    cart_queryset = Cart.objects.all()
    cart_item_queryset = CartItem.objects.all()
    return CartService(cart_queryset=cart_queryset, cart_item_queryset=cart_item_queryset)
