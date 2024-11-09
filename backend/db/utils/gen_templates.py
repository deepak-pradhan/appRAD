from sqlalchemy import MetaData, Table, Column, Integer, String, Text, ForeignKey
from sqlalchemy.schema import PrimaryKeyConstraint, UniqueConstraint
import json

# Create a MetaData instance
metadata = MetaData()

# Define the users table
users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(50), nullable=False, unique=True),
    Column('email', String(120), nullable=False, unique=True)
)

# Define the posts table
posts = Table('posts', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(200), nullable=False),
    Column('content', Text, nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
)

# Function to convert SQLAlchemy Table to JSON structure
def table_to_json(table):
    json_table = {
        "name": table.name,
        "columns": [],
        "constraints": [],
        "indexes": []
    }
    
    for column in table.columns:
        json_column = {
            "name": column.name,
            "type": str(column.type),
            "nullable": column.nullable
        }
        if column.primary_key:
            json_column["primary_key"] = True
        if column.unique:
            json_column["unique"] = True
        json_table["columns"].append(json_column)
    
    for constraint in table.constraints:
        if isinstance(constraint, PrimaryKeyConstraint):
            json_table["constraints"].append({
                "type": "PrimaryKeyConstraint",
                "columns": [col.name for col in constraint.columns]
            })
        elif isinstance(constraint, UniqueConstraint):
            json_table["constraints"].append({
                "type": "UniqueConstraint",
                "columns": [col.name for col in constraint.columns]
            })
        elif isinstance(constraint, ForeignKey):
            json_table["constraints"].append({
                "type": "ForeignKeyConstraint",
                "columns": [constraint.parent.name],
                "referred_table": constraint.column.table.name,
                "referred_columns": [constraint.column.name]
            })
    
    return json_table

# Convert metadata to our JSON structure
json_metadata = {
    "metadata": {
        "schema_name": "example_schema",
        "tables": [table_to_json(table) for table in metadata.tables.values()]
    }
}

# Print the JSON representation
print(json.dumps(json_metadata, indent=2))