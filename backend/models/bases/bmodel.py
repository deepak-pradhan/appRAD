"""
`BModel` an abstract base class that inherits from both `ABC` (Abstract Base Class) and `SQLModel`. 

It has:
    1. Pre-defined fields of Thing: 
       `id`, `type`, `name`, `description`

    2. Blammable fields: 
       `created_at`, `updated_at`

    3. Basis State: 
       `is_active`
"""
from abc import ABC, abstractmethod
from typing import List, TypeVar 
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

T = TypeVar('T', bound='BModel')

class BModel(ABC, SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    type: str | None = Field(default=None, description="Type of the record/object")
    name: str | None = Field(description="Name of the item")
    description: str | None = Field(default=None, description="Description of the item")    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True

    class Config:
        arbitrary_types_allowed = True  # Allows for more flexible type definitions


    @abstractmethod
    def validate(self) -> None:
        """Enforce all extended model: Must have a name """
        if not self.name:
            raise ValueError("Name cannot be empty")

    @classmethod
    def bulk_create(cls, session, objects: List["BModel"]):
        '''
        Provide all extended Models the ability to Bulk Create
        used_by: backend.utils.load_data
        '''
        for obj in objects:
            obj.validate()
        session.add_all(objects)
        session.commit()
        return objects