from django.db.models import QuerySet, Q

from apps.products.models import Product


class RecommendationService:
    def __init__(self, product_queryset: QuerySet[Product]):
        self.product_queryset = product_queryset

    def get_user_ordered_products(self, user_id: int, ) -> QuerySet[Product]:
        """
        Returns all sellable products ordered by the user
        """
        excluded_statuses = ["cancelled", "pending", "returned"]

        products = self.product_queryset.filter(
            orderitem__order__user_id=user_id,
            orderitem__order__archived=False,
            stock__gt=0,
            for_sale=True,
        ). \
        exclude(
            orderitem__order__status__in=excluded_statuses,
        ).order_by('-price').distinct()

        return products
