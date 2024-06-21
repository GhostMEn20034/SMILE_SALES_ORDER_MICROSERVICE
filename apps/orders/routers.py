from rest_framework.routers import SimpleRouter, Route

class OrderRouter(SimpleRouter):
    routes = [
        Route(
            url='{prefix}/',
            mapping={
                'post': 'create',
            },
            name="{basename}-list",
            detail=False,
            initkwargs={'suffix': 'List'}

        ),
    ]