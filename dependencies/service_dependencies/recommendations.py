from apps.products.models import Product
from services.recommendations.recommendation_service import RecommendationService


def get_recommendation_service() -> RecommendationService:
    product_queryset = Product.objects.all()

    return RecommendationService(product_queryset)