from typing import Dict, List

from django.db.models import QuerySet

from apps.addresses.models import Address
from apps.addresses.serializers.api_serializers import AddressSerializer


class AddressService:
    def __init__(self, address_queryset: QuerySet[Address]):
        self.address_queryset = address_queryset

    def get_addresses(self, user_id: int) -> List[Dict]:
        addresses = self.address_queryset.filter(user_id=user_id)
        serializer = AddressSerializer(addresses, many=True)
        return serializer.data

