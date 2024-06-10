import logging

from apps.addresses.serializers.replication import AddressReplicationSerializer

class AddressCreator:
    """
    Responsible for creating addresses with the data sent by the other server via message broker.
    """
    @staticmethod
    def create_one_address(data: dict) -> dict:
        serializer = AddressReplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.validated_data
        else:
            logging.error(serializer.errors)
            logging.info("Unable to serialize data and create an Address")
