from typing import Any

from .replication.create import AccountCreator
from .replication.update import AccountModifier

def handle_account_queue_message(routing_key: str, message: Any):
    if routing_key == 'users.accounts.create.one':
        return AccountCreator().create_one(message)
    elif routing_key == 'users.accounts.update.one':
        return AccountModifier().update_one(message)
