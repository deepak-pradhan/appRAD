from pathlib import Path
from backend.examples.common.schemas.person.person import person_schema

# Read Cerberus Schema from backend/examples/common/schemas/*
# Example person.py


# write a function that reads the person_schema and convert to CSV file header
def flatten_schema(schema, parent_key='', sep='_'):
    """Flatten a nested schema dictionary for CSV headers."""
    items = []
    for key, value in schema.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if value.get('type') == 'dict' and 'schema' in value:
            # Recursively flatten nested dictionaries
            items.extend(flatten_schema(value['schema'], new_key, sep=sep))
        else:
            items.append(new_key)
    return items

import csv

def save_header(items):
    """Save flattened schema headers to CSV file"""
    output_dir = Path('backend/examples/common/file_headers')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / 'header_of_person.csv'
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(items)


# Example Usage
items = flatten_schema(person_schema)
save_header(items)
# print(csv_headers)


