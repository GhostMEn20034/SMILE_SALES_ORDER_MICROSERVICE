from apps.products.serializers.api_serializers import ProductPublicDataSerializer
from apps.core.views import CustomAuthenticatedBaseViewSet
from dependencies.service_dependencies.recommendations import get_recommendation_service
from services.recommendations.recommendation_service import RecommendationService


class RecommendationViewSet(CustomAuthenticatedBaseViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recommendation_service: RecommendationService = get_recommendation_service()

    def get_bought_products(self, request, *args, **kwargs):
        products = self.recommendation_service.get_user_ordered_products(request.user.id)
        page = self.paginator.paginate_queryset(products, request)

        serializer = ProductPublicDataSerializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)




