from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('', include('apps.orders.urls')),
        path('', include('apps.payments.urls')),
        path('', include('apps.webhooks.urls')),
    ])),
]
