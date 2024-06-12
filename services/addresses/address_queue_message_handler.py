from typing import Any

from .replication.create import AddressCreator
from .replication.update import AddressModifier
from .replication.delete import AddressRemover

def handle_address_queue_message(routing_key: str, message: Any):
    if routing_key == 'users.addresses.create.one':
        return AddressCreator.create_one_address(message)
    elif routing_key == 'users.addresses.update.one':
        return AddressModifier.update_one_address(message)
    elif routing_key == 'users.addresses.delete.one':
        return AddressRemover.remove_one_address(message)
