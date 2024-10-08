from sqlmodel import Field
from pydantic import EmailStr
from sqlalchemy.orm import declared_attr
from backend.models.base import CModel

class Vendor(CModel, table=True):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() # Auto-create Table Name:= lower(Model Name)
    
    type: str = "vendor"  
    name: str = Field(index=False)          
    email: EmailStr = Field(default=None)
    
    def validate(self) -> None:
        if not self.name:
            raise ValueError("Name cannot be empty")
        if not self.email:
            raise ValueError("Email cannot be empty")
