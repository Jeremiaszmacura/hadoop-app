"""AddressData database model."""
from flaskr.models.db import fernet


class AddressData:
    """Class of AddressData database model"""

    colection_name = "address_data"

    def __init__(
        self,
        address: str,
        nested_addresses: list = None,
        words: list = None,
        encrypted: bool = False,
    ):
        self.address = address
        self.nested_addresses = nested_addresses
        self.words = words
        self.encrypted = encrypted

    def encrypt(self):
        """Encrypt object."""
        encrypted_nested_addresses = []
        encrypted_words = []

        self.address = fernet.encrypt(self.address.encode())
        for adress in self.nested_addresses:
            encrypted_nested_addresses.append(fernet.encrypt(adress.encode()))
        for words in self.words:
            encrypted_words.append(fernet.encrypt(words.encode()))

        self.nested_addresses = encrypted_nested_addresses
        self.words = encrypted_words
        self.encrypted = True

    def decrypt(self):
        """Decrypt object."""
        decrypted_nested_addresses = []
        decrypted_words = []

        self.address = fernet.decrypt(self.address).decode()
        for adress in self.nested_addresses:
            decrypted_nested_addresses.append(fernet.decrypt(adress).decode())
        for words in self.words:
            decrypted_words.append(fernet.decrypt(words).decode())

        self.nested_addresses = decrypted_nested_addresses
        self.words = decrypted_words
        self.encrypted = False
