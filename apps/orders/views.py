import uuid

from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from apps.orders.serializers.request_body_serializers import OrderCreationRequestBody, OrderListFiltersRequestBody, \
    ChangeArchivedStatusRequestBody
from apps.orders.serializers.api_serializers import OrderSerializer
from apps.core.pagination import CustomPagination
from param_classes.orders.change_archived_status import ChangeArchivedStatusParams
from .serializers.api_detailed_serializers import OrderListSerializer, OrderDetailsSerializer
from dependencies.service_dependencies.orders import get_order_service
from dependencies.mediator_dependencies.order_processing import get_order_processing_coordinator
from mediators.order_processing_coordinator import OrderProcessingCoordinator
from param_classes.orders.order_list import OrderListParams
from services.orders.order_service import OrderService
from param_classes.order_processing_coordinator.order_creation import OrderCreationParams
from param_classes.order_processing_coordinator.order_cancelation import OrderCancellationParams


class OrderViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination


    lookup_field = 'order_uuid'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_service: OrderService = get_order_service()
        self.order_processing_coordinator: OrderProcessingCoordinator = get_order_processing_coordinator(
            order_service=self.order_service)

    def create(self, request, *args, **kwargs) -> Response:
        serializer = OrderCreationRequestBody(data={
            'cart_owner_id': request.user.id,
            'address_id': request.data['address_id'],
            'product_ids': request.data['product_ids'],
        })
        serializer.is_valid(raise_exception=True)

        order_creation_params: OrderCreationParams = OrderCreationParams(**serializer.validated_data)
        payment_data = self.order_processing_coordinator.create_order_and_initialize_payment(order_creation_params)
        return Response(
            data={
                'payment_id': payment_data.payment_id,
                'checkout_link': payment_data.checkout_link,
            },
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs) -> Response:
        order_status = request.query_params.get('order_status')
        time_filter = request.query_params.get('time_filter')

        serializer = OrderListFiltersRequestBody(data={
            "order_status": order_status, "time_filter": time_filter
        })
        serializer.is_valid(raise_exception=True)

        order_list_params = OrderListParams(
            user_id=request.user.id,
            order_status=order_status,
            time_filter=time_filter,
        )
        order_list = self.order_service.get_orders(order_list_params)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(order_list, request)
        if page is not None:
            serializer = OrderListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = OrderListSerializer(order_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_order_creation_essentials(self, request, *args, **kwargs) -> Response:
        order_creation_essentials = self.order_processing_coordinator.get_order_creation_essentials(
            user_id=request.user.id,
        )
        return Response(
            data={
                "addresses": order_creation_essentials.addresses,
            },
            status=status.HTTP_200_OK,
        )

    def cancel_order(self, request, order_uuid: uuid.UUID, *args, **kwargs) -> Response:
        order_cancellation_params = OrderCancellationParams(
            order_uuid=order_uuid,
        )
        modified_order = self.order_processing_coordinator.cancel_order(order_cancellation_params)
        serializer = OrderSerializer(instance=modified_order)

        return Response(data={"order": serializer.data}, status=status.HTTP_200_OK)

    def get_order_list_filters(self, request, *args, **kwargs) -> Response:
        order_status = request.query_params.get('order_status')
        filters = self.order_service.get_order_list_filters(order_status)
        return Response(
            data={
                "filters": filters,
            },
            status=status.HTTP_200_OK,
        )

    def get_order_by_uuid(self, request, order_uuid: uuid.UUID, *args, **kwargs) -> Response:
        order = self.order_service.get_order_details(request.user.id, order_uuid)
        serializer = OrderDetailsSerializer(instance=order)
        return Response(data={"order": serializer.data}, status=status.HTTP_200_OK)

    def change_order_archive_flag(self, request, order_uuid: uuid.UUID, *args, **kwargs) -> Response:
        """
        Order archival method
        """
        purpose = request.data.get('purpose', 'archive')

        serializer = ChangeArchivedStatusRequestBody(data={"purpose": purpose})
        serializer.is_valid(raise_exception=True)

        change_archived_status_params = ChangeArchivedStatusParams(
            user_id=request.user.id,
            order_uuid=order_uuid,
            purpose=serializer.validated_data.get('purpose'),
        )

        order = self.order_service.change_archived_flag(change_archived_status_params)
        return Response(
            data={'archived': order.archived, }
        )
