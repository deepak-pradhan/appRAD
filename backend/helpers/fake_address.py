from faker import Faker
fake = Faker()

class Address:
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
        
    def generate_address(self):
        self.full_address= f"{self.building} {self.street_name}, {self.city}, {self.state} - {self.postal}"

    def validate(self) -> None:
        super().validate()
        if self.state not in self.country:
            raise ValueError(f"Un-synthetic state {self.state} in {self.country}")
        
    def generate(self):
        return self