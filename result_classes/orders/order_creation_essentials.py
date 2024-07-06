from typing import List, Dict


class OrderCreationEssentialsParams:
    """
    Class to hold all parameters to get order creation essentials.
    """
    def __init__(self, addresses: List[Dict]):
        self.addresses = addresses
