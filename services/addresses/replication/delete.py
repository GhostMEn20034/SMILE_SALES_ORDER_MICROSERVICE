import logging

from apps.addresses.models import Address


class AddressRemover:
    """
    Responsible for deleting addresses with the data sent by the other server via message broker.
    """
    @staticmethod
    def remove_one_address(data: dict) -> None:
        try:
            address = Address.objects.get(original_id=data.pop("address_id"))
        except Address.DoesNotExist:
            logging.error("Cannot find product to update")
            return None

        address.user = None
        address.save()
