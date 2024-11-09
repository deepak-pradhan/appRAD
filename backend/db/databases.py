from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///backend.db"
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session

def get_json():
    pass

__all__ = ['get_db', 'create_db_and_tables']       