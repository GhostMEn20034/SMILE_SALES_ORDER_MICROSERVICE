from typing import Optional, List


class CartItemFilters:
    def __init__(self, cart_owner_id: int, product_ids: Optional[List[str]] = None, include_only_saleable = False):
        # ID of cart's owner
        self.cart_owner_id = cart_owner_id
        # List of products ids
        self.product_ids = product_ids
        # If False, then the program must include the All Cart items
        # If True, cart item with ONLY SELLABLE (stock > 0 and for_sale = True, cart_item.quantity <= product.stock)
        # products must be included.
        self.include_only_saleable = include_only_saleable
