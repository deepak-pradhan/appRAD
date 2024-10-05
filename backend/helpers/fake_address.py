from faker import Faker
fake = Faker()


class Address:
    """
    Address:
        address()
        city()
        state()
        country()
        postcode()
        street_address()
    """
    def __init__(self, max=1):
        self.generated = set()
        self.max = max
        self.street_name = fake.street_name()
        self.building = fake.building_number()
        self.street_address = f"{self.building} {self.street_name}"
        self.city = fake.city()
        self.state = fake.state()
        self.country = fake.country()
        self.postal = fake.postal_code()

        self.generate_address(self, self.max)
        
    def generate_address(self, max):
        self.full_address= f"{self.building} {self.street_name}, {self.city}, {self.state} - {self.postal}"
        
    def generate(self):
        return self