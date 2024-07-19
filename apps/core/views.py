from rest_framework import viewsets, permissions

from .pagination import CustomPagination


class CustomAuthenticatedBaseViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            self._paginator = self.pagination_class()

        return self._paginator

    def paginate_queryset(self, queryset):
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data)
