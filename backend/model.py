from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession

Base = declarative_base()

class BaseMixin:
    id = Column(Integer, primary_key=True)

class Tenant(Base, BaseMixin):
    __tablename__ = 'tenants'

    name = Column(String(255), nullable=False)

    def validate_name(cls, value):
        if len(value) < 3 or len(value) > 25:
            raise ValueError("Name must be between 3 and 25 characters")

    def __init__(self, **kwargs):
        super().__init__()
        self.validate_name(kwargs.get('name'))
        for key, value in kwargs.items():
            setattr(self, key, value)

    # Define some helper functions for working with the database
    async def all(db):
        return await db.query(Tenant).all()

    async def get(cls, id: int, db: AsyncSession):
        return await db.query(Tenant).get(id)

    async def save(obj, db):
        db.add(obj)
        await db.commit()
        await db.refresh(obj)

    async def delete(obj, db):
        db.delete(obj)
        await db.commit()