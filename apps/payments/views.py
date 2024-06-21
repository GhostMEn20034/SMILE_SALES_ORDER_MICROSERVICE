from rest_framework import viewsets, permissions
from rest_framework.decorators import action


class PaymentViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)


    @action(detail=True, methods=['POST'])
    def capture_payment(self, request, payment_id):
        pass
