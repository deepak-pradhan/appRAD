import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('./../data/backend.db')
cursor = conn.cursor()

# Create Tenant table
tenant_table = """
CREATE TABLE IF NOT EXISTS Tenant (
    tenant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
"""
cursor.execute(tenant_table)

# Create Category table
category_table = """
CREATE TABLE IF NOT EXISTS Category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    tenant_id INTEGER,
    FOREIGN KEY (tenant_id) REFERENCES Tenant(tenant_id)
);
"""
cursor.execute(category_table)

# Create Product table
product_table = """
CREATE TABLE IF NOT EXISTS Product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    category_id INTEGER,
    tenant_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES Category(id),
    FOREIGN KEY (tenant_id) REFERENCES Tenant(tenant_id)
);
"""
cursor.execute(product_table)

# Commit changes and close the connection
conn.commit()
conn.close()
