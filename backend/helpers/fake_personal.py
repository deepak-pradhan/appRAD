from dataclasses import dataclass
from faker import Faker
from backend.helpers import Address, Email
fake = Faker()


class Personal:
    """
    Personal:
        name()
        first_name()
        last_name()
        prefix()
        suffix()
        email()
        phone_number()
        date_of_birth()
        ssn()
    """   
    def __init__(self):
        self.generated = set()
        self.name = fake.name()
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.prefix = fake.prefix()
        self.suffix = fake.suffix()
        self.email = Email.generate_personal_email(self.first_name, self.last_name)
        self.phone_number = fake.phone_number()
        self.date_of_birth = fake.date_of_birth()
        self.ssn = fake.ssn()

        self.job = fake.job()
        self.company = fake.company()
        self.address = Address()
        self.company_email = Email.generate_company_email(self.company)
        
    def _generator(self):

        first_name = fake.first_name()
        last_name = fake.last_name()
        
        data = {
                "name" : f"{first_name} {last_name}"
                , "first_name": first_name
                , "last_name": last_name
                , "prefix" : '?'
                , "suffix" : '?'
                , "email" : fake.email()
                , "phone_number" : ''
                , "date_of_birth" : ''
                , "ssn" : ''
            }
        self.generated = data
        return True
        
        
    def generate(self):
        if self._generator():
            return self.generated