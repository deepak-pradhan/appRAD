import random
from faker import Faker
from backend.helpers.fake_address import Address
fake = Faker()


class Company(Address):
    """
    Company:
        company()
        industry()
        catch_phrase()

    Company belongsTo:
        industry = ['Automotive','Health Care','Manufacturing','High Tech','Retail']    
    """
    def __init__(self):
        super.__init__(max=1)
        self.generated = set()
        self.name = fake.company()
        self.name_suffix = fake.company_suffix()
        self.full_address = self.full_address
        self.street_address = self.street_address
        self.city = self.city
        self.state = self.state
        self.postal = self.postal

    def _generate_address(self):
        self.generated = (('id', 123), ('address', 'some-address'))
        
    def generate(self):
        return self.generated