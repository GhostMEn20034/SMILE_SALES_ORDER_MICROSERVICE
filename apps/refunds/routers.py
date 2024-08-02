from rest_framework.routers import SimpleRouter, Route


class RefundRouter(SimpleRouter):
    routes = [
        Route(
            url=r'{prefix}/$',
            mapping={
                'post': 'create_refund_request',
            },
            name="{basename}-list",
            detail=False,
            initkwargs={'suffix': 'List'}

        ),
    ]