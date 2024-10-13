from abc import ABC, abstractmethod
from typing import List, TypeVar 
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

T = TypeVar('T', bound='CModel')

class CModel(ABC, SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    type: str | None = None
    name: str | None = None
    description: str | None = None
    
    # Blamables
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # created_by: str | None = None
    # updated_by: str | None = None

    # Lifecycle
    # start_at: datetime | None = None
    # ended_at: datetime | None = None
    # is_active: bool = True
    # is_deleted: bool = False
    # purge_on: datetime | None = None
    # status: str = 'S00'
    # version: int = 1

    class Config:
        arbitrary_types_allowed = True  # Allows for more flexible type definitions

    @abstractmethod
    def validate(self) -> None:
        pass

    @classmethod
    def bulk_create(cls, session, objects: List["CModel"]):
        for obj in objects:
            obj.validate()
        session.add_all(objects)
        session.commit()
        return objects