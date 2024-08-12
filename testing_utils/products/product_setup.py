from typing import List

from apps.products.factories import ProductFactory
from apps.products.models import Product


class ProductSetupInitializer:
    """
    Sets up and configures the components related to the "Product" entity for tests.
    """
    @staticmethod
    def get_products() -> List[Product]:
        # Use factory to build and save fake versions of the "Product" model
        products: List[Product] = ProductFactory.create_batch(10)
        return products

    @staticmethod
    def update_product_availability(product: Product, new_stock: int, for_sale: bool):
        product.stock = new_stock
        product.for_sale = for_sale
        product.save()
