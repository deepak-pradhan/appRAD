from backend.models.vendor import Vendor
from backend.models.product import Product
from backend.db.db_init import get_db
from faker import Faker
from backend.helpers import Address, Email, Personal
from backend.helpers.product_generator import generate_multiple_products

fake = Faker()
email_gen = Email()      

"""
print(fake.date_this_century().strftime('%m-%d-%Y'))
print(fake.date_this_decade().strftime('%m-%d-%Y'))
print(fake.date_this_year().strftime('%m-%d-%Y'))
print(fake.date_this_month().strftime('%m-%d-%Y'))
print(fake.time())
"""

def load_data(num_vendors: int =15, num_products=50):

    db = next(get_db())

    # app hM Vendors
    vendors = []
    vendor_ids = []

    for i  in range(1, num_vendors):
        vendor = Vendor(
            id = i,
            name=fake.name(),
            # email=fake.company_email(),
            email=email_gen.generate_email(fake.name()),
        )
        vendor.validate()
        vendors.append(vendor)

    Vendor.bulk_create(db, vendors)    
    vendor_ids = [vendor.id for vendor in vendors]


    # Vendor hM Products
    products = []

    products = generate_multiple_products(num_products=25, vendor_ids = vendor_ids)
    for product in products:
        product.validate()

    Product.bulk_create(db, products)
        

