from rest_framework.routers import SimpleRouter, Route

class RecommendationRouter(SimpleRouter):
    routes = [
        Route(
            url=r'{prefix}/bought-products/$',
            mapping={
                'get': 'get_bought_products',
            },
            name='{basename}-get-bought-products',
            detail=False,
            initkwargs={'suffix': 'Bought Product List'},
        ),
    ]