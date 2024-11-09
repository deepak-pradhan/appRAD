from typing import Dict, List
from sqlmodel import inspect
from backend.db.databases import get_db

def get_tables() -> Dict[str, List[Dict[str, str]]]:
    db = next(get_db())
    inspector = inspect(db.bind)

    tables = {}
    for table_name in inspector.get_table_names():
        tables[table_name] = get_table_columns(table_name)
    return tables

def get_table_columns(table_name: str):
    db = next(get_db())
    inspector = inspect(db.bind)

    columns = []
    for column in inspector.get_columns(table_name):
        columns.append({
            "name": column["name"],
            "type": str(column["type"]),
            "nullable": column["nullable"],
            "default": str(column["default"]) if column["default"] is not None else None,
        })
    return columns

if __name__ == "__main__":
    print(get_tables())
    print(get_table_columns(table_name='vendor'))