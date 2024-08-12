from typing import List

from django.contrib.auth import get_user_model
from apps.carts.models import Cart, CartItem


Account = get_user_model()


class CartSetupInitializer:
    """
    Sets up and configures the components related to the "Cart" and "CartItem" entities for tests.
    """
    def __init__(self):
        self.cart_items_added = 0

    @staticmethod
    def create_cart(account: Account) -> Cart:
        cart = Cart.objects.create(
            user_id=account.original_id,
        )
        return cart

    def add_cart_item_to_the_cart(self, cart: Cart, product_id: str, quantity: int = 1) -> CartItem:
        """
        Creates cart item for specified cart.
        :param cart: Cart to which item should be added.
        :param product_id: product which should be related with the cart item.
        :param quantity: how many units of the product should be added.
        """
        cart_item = CartItem.objects.create(
            cart=cart,
            original_id=self.cart_items_added + 1,
            product_id=product_id,
            quantity=quantity,
        )

        self.cart_items_added += 1

        return cart_item

    def add_products_to_cart(self, cart: Cart, product_ids: List[str], quantity: int):
        """
        Add products to cart.

        product_ids: List of product IDs to add to cart
        quantity: Quantity of each product to add
        """
        for product_id in product_ids:
            self.add_cart_item_to_the_cart(cart, product_id, quantity)