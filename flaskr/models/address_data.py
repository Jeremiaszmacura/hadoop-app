"""AddressData database model."""
from flaskr.models.db import fernet


class AddressData:
    """Class of AddressData database model"""

    collection_name: str = "address_data"

    def __init__(
        self,
        address: str,
        nested_addresses: list = None,
        words: list = None,
        encrypted: bool = False,
    ):
        self.address = address
        self.nested_addresses = nested_addresses or []
        self.words = words or []
        self.encrypted = encrypted

    def encrypt(self):
        """Encrypt object."""
        encrypted_nested_addresses: list = []
        encrypted_words: list = []

        self.address: list = fernet.encrypt(self.address.encode())
        for adress in self.nested_addresses:
            encrypted_nested_addresses.append(fernet.encrypt(adress.encode()))
        for words in self.words:
            encrypted_words.append(fernet.encrypt(words.encode()))

        self.nested_addresses: list = encrypted_nested_addresses
        self.words: list = encrypted_words
        self.encrypted: bool = True

    def decrypt(self):
        """Decrypt object."""
        decrypted_nested_addresses: list = []
        decrypted_words: list = []

        self.address: list = fernet.decrypt(self.address).decode()
        for adress in self.nested_addresses:
            decrypted_nested_addresses.append(fernet.decrypt(adress).decode())
        for words in self.words:
            decrypted_words.append(fernet.decrypt(words).decode())

        self.nested_addresses: list = decrypted_nested_addresses
        self.words: list = decrypted_words
        self.encrypted: bool = False
