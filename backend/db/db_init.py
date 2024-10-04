from backend.db.databases import get_db, create_db_and_tables

def init_db():
    get_db()
    create_db_and_tables()


