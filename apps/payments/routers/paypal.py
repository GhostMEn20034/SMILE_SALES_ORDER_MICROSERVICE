from rest_framework.routers import SimpleRouter, Route

class PayPalPaymentRouter(SimpleRouter):
    routes = [
        Route(
            url='{prefix}/{lookup}/capture/',
            mapping={
                'post': 'capture_payment',
            },
            name="{basename}-perform-capture",
            detail=True,
            initkwargs={}
        ),
    ]
