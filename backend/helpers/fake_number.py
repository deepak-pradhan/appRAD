import random
from faker import Faker
fake = Faker()


class Numbers:
    """
    Numbers:
        random_digit()
        random_int()
        random_element()
        random_elements()
    """
    def __init__(self):
        self.generated = set()

    def _generate_address(self):
        self.generated = (('id', 123), ('address', 'some-address'))
        
    def generate(self):
        return self.generated