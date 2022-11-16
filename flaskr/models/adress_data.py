"""AdressData database model."""

class AdressData():
    """Class of AdressData database model"""

    colection_name = "adress_data"

    def __init__(self, adress: str, words: list):
        self.adress = adress
        self.words = words
