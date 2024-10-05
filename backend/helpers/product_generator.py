from faker import Faker
import random
from backend.models.product import Product
fake = Faker()

"""
Product is a Subject Area
Product belongsTo Many Categories
"""

# You can expand this list based on your needs
CATEGORIES = ['Electronics', 'Clothing', 'Books', 'Home & Kitchen', 'Sports & Outdoors', 'Toys & Games']

def generate_synthetic_product(vid: int = None) -> Product:
    category = random.choice(CATEGORIES)
    
    if category == 'Electronics':
        name = fake.word() + ' ' + random.choice(['Smartphone', 'Laptop', 'Tablet', 'Headphones', 'Smart Watch'])
    elif category == 'Clothing':
        name = fake.color_name() + ' ' + random.choice(['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Shoes'])
    elif category == 'Books':
        name = fake.catch_phrase() + ' (Book)'
    elif category == 'Home & Kitchen':
        name = fake.word() + ' ' + random.choice(['Blender', 'Coffee Maker', 'Toaster', 'Vacuum Cleaner', 'Cookware Set'])
    elif category == 'Sports & Outdoors':
        name = fake.word() + ' ' + random.choice(['Bicycle', 'Tennis Racket', 'Yoga Mat', 'Camping Tent', 'Running Shoes'])
    else:  # Toys & Games
        name = fake.word() + ' ' + random.choice(['Board Game', 'Action Figure', 'Puzzle', 'Building Blocks', 'Remote Control Car'])

    return Product(
        name=name,
        description=fake.paragraph(nb_sentences=3),
        price=round(random.uniform(9.99, 999.99), 2),
        category=category,
        sku=fake.ean(length=13),
        stock=random.randint(0, 1000),
        vendor_id=vid
    )

def generate_multiple_products(num_products: int, vendor_ids: list[int] = None) -> list[Product]:
    products = []
    for vendor_id in vendor_ids:
        for i in range(1, num_products):
            products.append(generate_synthetic_product(vendor_id+1))
            print(f"vid={vendor_id} and i={i}")
    return products
