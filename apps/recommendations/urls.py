from .routers import RecommendationRouter
from .views import RecommendationViewSet

router = RecommendationRouter()

router.register('recommendations', RecommendationViewSet, basename='recommendations')

urlpatterns = router.urls
