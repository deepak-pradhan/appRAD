import random
from faker import Faker
fake = Faker()


class Email:
    def __init__(self):
        self.generated_emails = set()

    def _syntheic_email(self, first_name, last_name, domain_func, company=None):
        while True:
            email_format = random.choice([
                "{first}{last}",
                "{first}.{last}",
                "{first_initial}{last}",
                "{first}_{last}",
                "{last}{first_initial}"
            ])
            
            email_name = email_format.format(
                first=first_name.lower(),
                last=last_name.lower(),
                first_initial=first_name[0].lower()
            )
            
            if email_name in self.generated_emails:
                email_name += str(random.randint(1, 99))
            
            domain = domain_func(company) if company else domain_func()
            email = f"{email_name}@{domain}"
            
            if email not in self.generated_emails:
                self.generated_emails.add(email)
                return email

    def generate_company_email(self, first_name, last_name, company):
        def company_domain(company):
            return company.lower().replace(' ', '') + '.com'
        return self._syntheic_email(first_name, last_name, company_domain, company)

    def generate_personal_email(self, first_name, last_name):
        return self._syntheic_email(first_name, last_name, fake.free_email_domain)