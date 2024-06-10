import logging

from apps.carts.models import CartItem, Cart


class CartRemover:
    """
    Responsible for deleting carts / cart items with the data sent by the other server via message broker.
    """
    @staticmethod
    def clear_cart(data: dict) -> None:
        cart_uuid = data.pop("cart_uuid")
        cart = Cart.objects.get(cart_uuid=cart_uuid)
        cart.clear()

    @staticmethod
    def remove_one_cart_item(data: dict) -> None:
        try:
            cart_item = CartItem.objects.get(original_id=data.pop("original_id"))
        except CartItem.DoesNotExist:
            logging.error("Cannot find product to update")
            return None

        cart_item.delete()