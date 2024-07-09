from rest_framework import viewsets
from rest_framework.response import Response

from dependencies.mediator_dependencies.order_processing import get_order_processing_coordinator
from mediators.order_processing_coordinator import OrderProcessingCoordinator


class WebhookViewSet(viewsets.ViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_processing_coordinator: OrderProcessingCoordinator = get_order_processing_coordinator()

    def paypal(self, request, *args, **kwargs):
        event_type = request.data.get('event_type')
        print(f'PayPal webhook event type: {event_type}')
        return Response({"status": "success"})
