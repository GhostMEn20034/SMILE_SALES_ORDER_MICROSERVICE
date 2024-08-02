from .routers import RefundRouter
from .views import RefundsViewSet

router = RefundRouter()

router.register('refunds', RefundsViewSet, basename='refunds')

urlpatterns = router.urls