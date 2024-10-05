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

    # def soft_delete(self):
    #     """Mark the record as deleted without removing it from the database"""
    #     self.is_deleted = True
    #     self.is_active = False
    #     self.ended_date = datetime.now(timezone.utc)
    #     self.updated_at = datetime.now(timezone.utc)

    # def restore(self):
    #     """Restore a soft-deleted record"""
    #     self.is_deleted = False
    #     self.is_active = True
    #     self.ended_date = None
    #     self.updated_at = datetime.now(timezone.utc)

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

    # @classmethod
    # def get(cls: Type[T], session: Session, id: int) -> Optional[T]:
    #     """Retrieve a model instance by its ID"""
    #     return session.get(cls, id)

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

    # @classmethod
    # def get_active(cls: Type[T], session: Session) -> List[T]:
    #     """Retrieve all active model instances"""
    #     return session.exec(
    #         select(cls)
    #             .where(
    #                 cls.is_active == True,
    #                 cls.ended_date == None)
    #         ).all()

    # @classmethod
    # def get_by_date_range(cls: Type[T], session: Session, start: datetime, end: datetime) -> List[T]:
    #     """Retrieve model instances within a given date range"""
    #     return session.exec(
    #         select(cls)
    #             .where(
    #                 cls.start_date >= start,
    #                 cls.ended_date <= end)
    #         ).all()

    # def is_current(self) -> bool:
    #     """Check if the model instance is currently valid"""
    #     now = datetime.now(timezone.utc)
    #     return self.start_date <= now and (self.ended_date is None or self.ended_date > now)

    # @classmethod
    # def paginate(cls: Type[T]
    #              , session: Session
    #              , page: int = 1
    #              , per_page: int = 20
    #              , **kwargs
    #         ) -> Dict[str, Any]:
    #     """Paginate query results"""
        
    #     query = select(cls)
    #     for key, value in kwargs.items():
    #         query = query.where(getattr(cls, key) == value)
        
    #     total = session.exec(select(cls)).count()
    #     items = session.exec(query.offset((page - 1) * per_page).limit(per_page)).all()
    #     return {
    #         "items": items,
    #         "page": page,
    #         "per_page": per_page,
    #         "total": total,
    #         "pages": (total + per_page - 1) 
    #     }

    # @classmethod
    # def advanced_query(cls: Type[T], session: Session, filters: List[Dict[str, Any]], order_by: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> List[T]:
    #     """Execute an advanced query with filters, ordering, and pagination"""
    #     query = select(cls)
    #     for filter_dict in filters:
    #         field = getattr(cls, filter_dict['field'])
    #         op = filter_dict['op']
    #         value = filter_dict['value']
    #         if op == 'eq':
    #             query = query.where(field == value)
    #         elif op == 'ne':
    #             query = query.where(field != value)
    #         elif op == 'gt':
    #             query = query.where(field > value)
    #         elif op == 'lt':
    #             query = query.where(field < value)
    #         elif op == 'ge':
    #             query = query.where(field >= value)
    #         elif op == 'le':
    #             query = query.where(field <= value)
    #         elif op == 'in':
    #             query = query.where(field.in_(value))
    #         elif op == 'not_in':
    #             query = query.where(~field.in_(value))
    #         elif op == 'like':
    #             query = query.where(field.like(value))
    #         elif op == 'ilike':
    #             query = query.where(field.ilike(value))

    #     if order_by:
    #         if order_by.startswith('-'):
    #             query = query.order_by(getattr(cls, order_by[1:]).desc())
    #         else:
    #             query = query.order_by(getattr(cls, order_by))

    #     if limit is not None:
    #         query = query.limit(limit)
    #     if offset is not None:
    #         query = query.offset(offset)

    #     return session.exec(query).all()
    # def refresh(self, session: Session):
    #     """Refresh the model instance from the database"""
    #     session.refresh(self)

    # @classmethod
    # def count(cls: Type[T], session: Session, **kwargs) -> int:
    #     """Count the number of instances matching the given criteria"""
    #     query = select(cls)
    #     for key, value in kwargs.items():
    #         query = query.where(getattr(cls, key) == value)
    #     return session.exec(select(cls)).count()

    # def validate_unique(self, session: Session, fields: List[str]):
    #     """Validate that the instance is unique based on the given fields"""
    #     query = select(self.__class__)
    #     for field in fields:
    #         query = query.where(getattr(self.__class__, field) == getattr(self, field))
    #     if self.id:
    #         query = query.where(self.__class__.id != self.id)
    #     existing = session.exec(query).first()
    #     if existing:
    #         raise ValueError(f"Instance with {', '.join(fields)} already exists.")

    # @classmethod
    # def get_with_related(cls: Type[T], session: Session, id: int, related_fields: List[str]) -> Optional[T]:
    #     """Retrieve a model instance with related fields eagerly loaded"""
    #     query = select(cls).options(*[joinedload(getattr(cls, field)) for field in related_fields])
    #     return session.exec(query.where(cls.id == id)).first()

    # @classmethod
    # def get_version(cls, session: Session, id: int, version: int) -> Optional['CModel']:
    #     """Retrieve a specific version of a model instance"""
    #     return session.exec(select(cls).where(cls.id == id, cls.version == version)).first()

    # def set_datetime(cls, v):
    #     """Validator to ensure datetime fields are set to UTC"""
    #     return datetime.now(timezone.utc) if v is None else v

    @classmethod
    def bulk_create(cls, session, objects: List["CModel"]):
        for obj in objects:
            obj.validate()
        session.add_all(objects)
        session.commit()
        return objects