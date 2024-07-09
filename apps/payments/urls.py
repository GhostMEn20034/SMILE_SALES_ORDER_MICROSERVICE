from django.urls import path, include

from apps.payments.routers.paypal import PayPalPaymentRouter
from apps.payments.views.paypal import PayPalPaymentViewSet

paypal_router = PayPalPaymentRouter()

paypal_router.register('paypal', PayPalPaymentViewSet, basename='paypal-payment')

urlpatterns = [
    path('payments/', include(paypal_router.urls)),
]
