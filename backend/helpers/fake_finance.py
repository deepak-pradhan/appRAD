import random
from faker import Faker
fake = Faker()


class Finance:
    """
    Finance:
        credit_card_number()
        credit_card_expire()
    """
    def __init__(self):
        self.generated = set()

    def _generate_address(self):
        self.generated = (('id', 123), ('address', 'some-address'))
        
    def generate(self):
        return self.generated