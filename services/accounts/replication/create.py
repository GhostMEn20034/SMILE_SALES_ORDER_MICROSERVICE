import logging

from apps.accounts.serializers.replication import AccountReplicationSerializer

class AccountCreator:
    """
    Responsible for creating accounts with the data sent by the other server via message broker.
    """
    @staticmethod
    def create_one(data: dict) -> dict:
        serializer = AccountReplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.validated_data
        else:
            logging.error(serializer.errors)
            logging.info("Unable to serialize data and create a User")
