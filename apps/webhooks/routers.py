from rest_framework.routers import SimpleRouter, Route


class WebhookRouter(SimpleRouter):
    routes = [
        Route(
            url=r'{prefix}/paypal/$',
            mapping={
                'post': 'paypal',
            },
            name="{basename}-paypal",
            detail=False,
            initkwargs={'suffix': 'Paypal'}

        ),
    ]