from rest_framework.routers import SimpleRouter, Route, DynamicRoute


class OrderRouter(SimpleRouter):
    routes = [
        Route(
            url=r'{prefix}/$',
            mapping={
                'post': 'create',
                'get': 'list',
            },
            name="{basename}-list",
            detail=False,
            initkwargs={'suffix': 'List'}

        ),
        Route(
            url=r'{prefix}/filters/$',
            mapping={
                'get': 'get_order_list_filters',
            },
            name="{basename}-list-filters",
            detail=False,
            initkwargs={'suffix': 'List Filters'},
        ),
        Route(
            url=r'{prefix}/creation-essentials/$',
            mapping={
                'get': 'get_order_creation_essentials',
            },
            name="{basename}-creation-essentials",
            detail=False,
            initkwargs={'suffix': 'Creation Essentials',},
        ),
        Route(
            url=r'{prefix}/{lookup}/cancel/$',
            mapping={
                'post': 'cancel_order',
            },
            name="{basename}-cancel-order",
            detail=False,
            initkwargs={'suffix': 'Cancel Order'}
        ),
        Route(
            url=r'{prefix}/{lookup}/$',
            mapping={
                'get': 'get_order_by_uuid',
            },
            name='{basename}-details',
            detail=True,
            initkwargs={'suffix': 'Details'}
        ),
    ]