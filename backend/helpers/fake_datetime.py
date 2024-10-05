from faker import Faker
fake = Faker()


class Datetime:
    """
    Datetime:
        date_this_century()
        date_this_decade()
        date_this_year()
        date_time_this_year()
        future_date()
        past_date()

    ref: https://strftime.org/
    print(fake.year())
    print(fake.month())
    print(fake.day_of_month())
    print(fake.day_of_week())
    print(fake.month_name())
    print(fake.past_date('-1y'))
    print(fake.future_date('+1d'))
    print(fake.date_this_century().strftime('%m-%d-%Y'))
    print(fake.date_this_decade().strftime('%m-%d-%Y'))
    print(fake.date_this_year().strftime('%m-%d-%Y'))
    print(fake.date_this_month().strftime('%m-%d-%Y'))
    print(fake.time())
    """
    def __init__(self):
        self.generated = set()

    def _generate_address(self):
        self.generated = (('id', 123), ('address', 'some-address'))
        
    def generate(self):
        return self.generated