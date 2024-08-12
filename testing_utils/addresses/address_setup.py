from typing import List
from django.contrib.auth import get_user_model

from apps.addresses.models import Address


Account = get_user_model()


class AddressSetupInitializer:
    """
    Sets up and configures the components related to the "Address" entity for tests.
    """
    @staticmethod
    def get_addresses(account: Account) -> List[Address]:
        phone_numbers = [
            "380632280795",
            "4997259178535",
            "4997259172734",
        ]

        addresses_before_insert = []
        for i in range(3):
            address = Address(
                original_id=i + 1,
                user_id=account.original_id,
                country="DE",
                first_name=account.first_name,
                last_name=account.last_name if account.last_name else "Test Last Name",
                phone_number=phone_numbers[i],
                city="City69",
                region="Region69",
                street="69 Street",
                house_number="69",
                apartment_number="",
                postal_code="1488",
            )
            addresses_before_insert.append(address)

        addresses_after_insert = Address.objects.bulk_create(addresses_before_insert)

        return addresses_after_insert
