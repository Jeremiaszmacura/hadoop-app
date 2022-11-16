"""AdressData database model."""

class AdressData():
    """Class of AdressData database model"""

    colection_name = "adress_data"

    def __init__(self, adress: str, nested_adresses: list = [], words: list = []):
        self.adress = adress
        self.nested_adresses = nested_adresses
        self.words = words
