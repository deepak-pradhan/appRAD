import sqlite3

def load_sample_data(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Synthetic sample data for Tenant table
    tenant_data = [
        ('Tenant A',),
        ('Tenant B',)
    ]
    cursor.executemany("INSERT INTO Tenant (name) VALUES (?);", tenant_data)

    # Synthetic sample data for Category table
    category_data = [
        ('Fruits', 'Various types of fruits', 1),  # tenant_id 1 for Tenant A
        ('Vegetables', 'Various types of vegetables', 1),  # tenant_id 1 for Tenant A
        ('Grains', 'Different types of grains', 2),  # tenant_id 2 for Tenant B
        ('Pesticides', 'Various agricultural pesticides', 2),  # tenant_id 2 for Tenant B
    ]
    cursor.executemany("INSERT INTO Category (name, description, tenant_id) VALUES (?, ?, ?);", category_data)

    # Synthetic sample data for Product table
    product_data = [
        ('Apple', 'Fresh apples', 1.2, 1, 1),  # category_id 1, tenant_id 1 (Fruits, Tenant A)
        ('Banana', 'Ripe bananas', 0.5, 1, 1),  # category_id 1, tenant_id 1 (Fruits, Tenant A)
        ('Carrot', 'Organic carrots', 0.8, 2, 1),  # category_id 2, tenant_id 1 (Vegetables, Tenant A)
        ('Potato', 'High-quality potatoes', 0.3, 2, 1),  # category_id 2, tenant_id 1 (Vegetables, Tenant A)
        ('Rice', 'Premium white rice', 0.9, 3, 2),  # category_id 3, tenant_id 2 (Grains, Tenant B)
        ('Wheat', 'Whole grain wheat', 0.6, 3, 2),  # category_id 3, tenant_id 2 (Grains, Tenant B)
        ('Pesticide A', 'Pesticide for insects', 5.0, 4, 2),  # category_id 4, tenant_id 2 (Pesticides, Tenant B)
        ('Pesticide B', 'Organic pesticide', 6.5, 4, 2),  # category_id 4, tenant_id 2 (Pesticides, Tenant B)
    ]
    cursor.executemany("INSERT INTO Product (name, description, price, category_id, tenant_id) VALUES (?, ?, ?, ?, ?);", product_data)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    db_file = './../data/backend.db'
    load_sample_data(db_file)
