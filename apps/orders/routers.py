from rest_framework.routers import SimpleRouter, Route, DynamicRoute


class OrderRouter(SimpleRouter):
    routes = [
        Route(
            url=r'{prefix}/$',
            mapping={
                'post': 'create',
            },
            name="{basename}-list",
            detail=False,
            initkwargs={'suffix': 'List'}

        ),
        Route(
            url='{prefix}/creation-essentials/$',
            mapping={
                'get': 'get_order_creation_essentials',
            },
            name="{basename}-creation-essentials",
            detail=False,
            initkwargs={'suffix': 'Creation Essentials',},
        ),
    ]