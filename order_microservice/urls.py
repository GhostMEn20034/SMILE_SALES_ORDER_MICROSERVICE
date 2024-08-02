from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, get_resolver

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('', include('apps.orders.urls')),
        path('', include('apps.payments.urls')),
        path('', include('apps.webhooks.urls')),
        path('', include('apps.recommendations.urls')),
        path('', include('apps.refunds.urls'))
    ])),
]
