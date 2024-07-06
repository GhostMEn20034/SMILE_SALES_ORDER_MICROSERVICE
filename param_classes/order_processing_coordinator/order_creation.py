from typing import Optional, List


class OrderCreationParams:
    """
    Params essential for order creation process
    """
    def __init__(self, cart_owner_id: int, address_id: int,
                 product_ids:  Optional[List[str]] = None):
        self.cart_owner_id = cart_owner_id
        self.address_id = address_id
        self.product_ids = product_ids