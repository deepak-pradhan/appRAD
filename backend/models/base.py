from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, Tuple, Type, TypeVar 
from datetime import datetime, timezone
import json
from sqlmodel import SQLModel, Session, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlmodel import Field, SQLModel

T = TypeVar('T', bound='CModel')

class CModel(ABC, SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    type: str | None = None
    name: str | None = None
    description: str | None = None
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # created_by: str | None = None
    # updated_by: str | None = None
    # start_date: int | None = None
    # ended_date: int | None = None
    # is_active: bool = True
    # is_deleted: bool = False
    # status: str = 'S00'
    # version: int = 1

    class Config:
        arbitrary_types_allowed = True  # Allows for more flexible type definitions

    @abstractmethod
    def validate(self) -> None:
        """isRequired: 
        Abstract method for custom validation logic
        """
        pass
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model instance to a dictionary"""
        return {field: getattr(self, field) for field in self.__fields__}

    def to_json(self) -> str:
        """Convert the model instance to a JSON string"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create a model instance from a dictionary"""
        return cls(**data)

    @classmethod
    def from_json(cls: Type[T], json_str: str) -> T:
        """Create a model instance from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def update(self, session: Session, **kwargs):
        """Update the model instance with new values"""
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        self.version += 1
        session.add(self)
        session.commit()
        session.refresh(self)

    def save(self, session: Session) -> None:
        """Save the model instance to the database"""
        session.add(self)
        try:
            session.commit()
            session.refresh(self)
        except IntegrityError as e:
            session.rollback()
            raise ValueError(f"Integrity error: {str(e)}") from e
        except Exception as e:
            session.rollback()
            raise ValueError(f"Error saving model: {str(e)}") from e

    def delete(self, session: Session):
        """Delete the model instance from the database"""
        session.delete(self)
        session.commit()

    @classmethod
    def find(cls: Type[T], session: Session, **kwargs) -> List[T]:
        """Find model instances based on given criteria"""
        query = select(cls)
        for key, value in kwargs.items():
            query = query.where(getattr(cls, key) == value)
        return session.exec(query).all()

    @classmethod
    def find_one(cls: Type[T], session: Session, **kwargs) -> Optional[T]:
        """Find a single model instance based on given criteria"""
        query = select(cls)
        for key, value in kwargs.items():
            query = query.where(getattr(cls, key) == value)
        return session.exec(query).first()

    @classmethod
    def bulk_create(cls, session, objects: List["CModel"]):
        for obj in objects:
            obj.validate()
        session.add_all(objects)
        session.commit()
        return objects