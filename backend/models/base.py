from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, Tuple, Type, TypeVar, Union
from datetime import datetime, timezone
import json
from sqlmodel import SQLModel, Session, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlmodel import Field, SQLModel

T = TypeVar('T', bound='CModel')

class CModel(ABC, SQLModel):
    # Common fields for all models
    id: int | None = Field(default=None, primary_key=True)
    rec_type: str | None = None  # Record type for polymorphic queries
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str | None = None  # User who created the record
    updated_by: str | None = None  # User who last updated the record
    start_date: int | None = None  # Start date for record validity
    ended_date: int | None = None  # End date for record validity
    is_active: bool = Field(default=True)  # Flag to indicate if the record is active
    is_deleted: bool = Field(default=False)  # Soft delete flag
    version: int = Field(default=1)  # Version number for optimistic locking

    class Config:
        arbitrary_types_allowed = True  # Allows for more flexible type definitions

    @abstractmethod
    def validate(self) -> None:
        """Abstract method for custom validation logic"""
        pass

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Abstract property for human-readable representation of the model"""
        pass

    @classmethod
    @abstractmethod
    def get_by_name(cls: Type[T], session: Session, name: str) -> Optional[T]:
        """Abstract method to retrieve a record by its name"""
        pass

    @staticmethod
    @abstractmethod
    def generate_unique_identifier() -> str:
        """Abstract method to generate a unique identifier for the model"""
        pass

    def __repr__(self):
        """String representation of the model instance"""
        return f"<{self.__class__.__name__}(id={self.id})>"

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

    @classmethod
    def bulk_create(cls: Type[T], items: List[Dict[str, Any]]) -> List[T]:
        """Create multiple model instances from a list of dictionaries"""
        return [cls.from_dict(item) for item in items]

    def set_datetime(cls, v):
        """Validator to ensure datetime fields are set to UTC"""
        return datetime.now(timezone.utc) if v is None else v

    def soft_delete(self):
        """Mark the record as deleted without removing it from the database"""
        self.is_deleted = True
        self.is_active = False
        self.ended_date = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def restore(self):
        """Restore a soft-deleted record"""
        self.is_deleted = False
        self.is_active = True
        self.ended_date = None
        self.updated_at = datetime.now(timezone.utc)

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
    def get(cls: Type[T], session: Session, id: int) -> Optional[T]:
        """Retrieve a model instance by its ID"""
        return session.get(cls, id)

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
    def get_active(cls: Type[T], session: Session) -> List[T]:
        """Retrieve all active model instances"""
        return session.exec(
            select(cls)
                .where(
                    cls.is_active == True,
                    cls.ended_date == None)
            ).all()

    @classmethod
    def get_by_date_range(cls: Type[T], session: Session, start: datetime, end: datetime) -> List[T]:
        """Retrieve model instances within a given date range"""
        return session.exec(
            select(cls)
                .where(
                    cls.start_date >= start,
                    cls.ended_date <= end)
            ).all()

    def is_current(self) -> bool:
        """Check if the model instance is currently valid"""
        now = datetime.now(timezone.utc)
        return self.start_date <= now and (self.ended_date is None or self.ended_date > now)

    @classmethod
    def paginate(cls: Type[T], session: Session, page: int = 1, per_page: int = 20, **kwargs) -> Dict[str, Any]:
        """Paginate query results"""
        query = select(cls)
        for key, value in kwargs.items():
            query = query.where(getattr(cls, key) == value)
        total = session.exec(select(cls)).count()
        items = session.exec(query.offset((page - 1) * per_page).limit(per_page)).all()
        return {
            "items": items,
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
        }

    @classmethod
    def advanced_query(cls: Type[T], session: Session, filters: List[Dict[str, Any]], order_by: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> List[T]:
        """Execute an advanced query with filters, ordering, and pagination"""
        query = select(cls)
        for filter_dict in filters:
            field = getattr(cls, filter_dict['field'])
            op = filter_dict['op']
            value = filter_dict['value']
            if op == 'eq':
                query = query.where(field == value)
            elif op == 'ne':
                query = query.where(field != value)
            elif op == 'gt':
                query = query.where(field > value)
            elif op == 'lt':
                query = query.where(field < value)
            elif op == 'ge':
                query = query.where(field >= value)
            elif op == 'le':
                query = query.where(field <= value)
            elif op == 'in':
                query = query.where(field.in_(value))
            elif op == 'not_in':
                query = query.where(~field.in_(value))
            elif op == 'like':
                query = query.where(field.like(value))
            elif op == 'ilike':
                query = query.where(field.ilike(value))

        if order_by:
            if order_by.startswith('-'):
                query = query.order_by(getattr(cls, order_by[1:]).desc())
            else:
                query = query.order_by(getattr(cls, order_by))

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        return session.exec(query).all()

    @classmethod
    def bulk_update(cls: Type[T], session: Session, items: List[Dict[str, Any]]):
        """Update multiple model instances in bulk"""
        for item in items:
            instance = session.get(cls, item['id'])
            if instance:
                for key, value in item.items():
                    if key != 'id':
                        setattr(instance, key, value)
                instance.updated_at = datetime.now(timezone.utc)
                instance.version += 1
        session.commit()

    @classmethod
    def get_or_create(cls: Type[T], session: Session, **kwargs) -> Tuple[T, bool]:
        """Get an existing instance or create a new one if it doesn't exist"""
        instance = cls.find_one(session, **kwargs)
        if instance:
            return instance, False
        else:
            instance = cls(**kwargs)
            instance.save(session)
            return instance, True

    def refresh(self, session: Session):
        """Refresh the model instance from the database"""
        session.refresh(self)

    @classmethod
    def count(cls: Type[T], session: Session, **kwargs) -> int:
        """Count the number of instances matching the given criteria"""
        query = select(cls)
        for key, value in kwargs.items():
            query = query.where(getattr(cls, key) == value)
        return session.exec(select(cls)).count()

    def validate_unique(self, session: Session, fields: List[str]):
        """Validate that the instance is unique based on the given fields"""
        query = select(self.__class__)
        for field in fields:
            query = query.where(getattr(self.__class__, field) == getattr(self, field))
        if self.id:
            query = query.where(self.__class__.id != self.id)
        existing = session.exec(query).first()
        if existing:
            raise ValueError(f"Instance with {', '.join(fields)} already exists.")

    @classmethod
    def get_with_related(cls: Type[T], session: Session, id: int, related_fields: List[str]) -> Optional[T]:
        """Retrieve a model instance with related fields eagerly loaded"""
        query = select(cls).options(*[joinedload(getattr(cls, field)) for field in related_fields])
        return session.exec(query.where(cls.id == id)).first()

    @classmethod
    def paginate_version(cls, session: Session, version: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Paginate query results for a specific version"""
        query = select(cls).where(cls.version == version)
        total = session.exec(select(cls).where(cls.version == version)).count()
        items = session.exec(query.offset((page - 1) * per_page).limit(per_page)).all()
        return {
            "items": items,
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
        }

    @classmethod
    def get_version(cls, session: Session, id: int, version: int) -> Optional['CModel']:
        """Retrieve a specific version of a model instance"""
        return session.exec(select(cls).where(cls.id == id, cls.version == version)).first()

    def create_new_version(self, session: Session):
        """Create a new version of the model instance"""
        new_version = self.copy(update={"version": self.version + 1})
        session.add(new_version)
        session.commit()
        return new_version