import logging
from sqlmodel import SQLModel, create_engine, Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///sbox1_backend.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def get_db():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

__all__ = ['get_db', 'create_db_and_tables']       