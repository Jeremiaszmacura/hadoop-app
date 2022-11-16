"""AddressData database model."""


class AddressData:
    """Class of AddressData database model"""

    colection_name = "address_data"

    def __init__(self, address: str, nested_addresses: list = [], words: list = []):
        self.address = address
        self.nested_addresses = nested_addresses
        self.words = words
