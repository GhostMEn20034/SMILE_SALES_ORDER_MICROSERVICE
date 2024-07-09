from .routers import WebhookRouter
from .views import WebhookViewSet

router = WebhookRouter()

router.register('webhooks', WebhookViewSet, basename='webhook')

urlpatterns = router.urls
