import logging
from typing import Optional
from django.contrib.auth import get_user_model
from apps.accounts.serializers.replication import AccountReplicationSerializer


User = get_user_model()

class AccountModifier:
    """
    Responsible for updating accounts with the data sent by the other server via message broker.
    """

    @staticmethod
    def update_one(data: dict) -> Optional[dict]:
        try:
            user = User.objects.get(original_id=data.pop("original_id"))
        except User.DoesNotExist:
            logging.error("Cannot find a user to update")
            return None

        data = AccountReplicationSerializer(instance=user, data=data, partial=True)
        if data.is_valid():
            data.save()
            return data.data
        else:
            logging.error(data.errors)
