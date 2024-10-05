import random
from faker import Faker
fake = Faker()


class Internet:
    """
    Internet:
        user_name()
        domain()
        url()
        ipv4()
        ipv6()
    """
    def __init__(self):
        self.generated = set()

    def _generate_address(self):
        self.generated = (('id', 123), ('address', 'some-address'))
        
    def generate(self):
        return self.generated