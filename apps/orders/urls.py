from .routers import OrderRouter
from .views import OrderViewSet

router = OrderRouter()

router.register('orders', OrderViewSet, basename='orders')

urlpatterns = router.urls
