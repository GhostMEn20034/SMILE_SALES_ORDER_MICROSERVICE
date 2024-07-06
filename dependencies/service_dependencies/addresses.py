from apps.addresses.models import Address
from services.addresses.address_service import AddressService


def get_address_service() -> AddressService:
    address_queryset = Address.objects.all()
    return AddressService(address_queryset)