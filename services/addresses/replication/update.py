import logging
from typing import Optional

from apps.addresses.models import Address
from apps.addresses.serializers.replication import AddressReplicationSerializer

class AddressModifier:
    """
    Responsible for updating addresses with the data sent by the other server via message broker.
    """
    @staticmethod
    def update_one_address(data: dict) -> Optional[dict]:
        try:
            address = Address.objects.get(original_id=data.pop("original_id"))
        except Address.DoesNotExist:
            logging.error("Cannot find an Address to update")
            return None

        data = AddressReplicationSerializer(instance=address, data=data, partial=True)
        if data.is_valid():
            data.save()
            return data.data
        else:
            logging.error(data.errors)
