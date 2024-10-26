from typing import List
from sqlmodel import Field, Relationship
from pydantic import EmailStr
from sqlalchemy.orm import declared_attr
from sbox1.backend.models.bases.bmodel import BModel

class Vendor(BModel, table=True):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() # Auto-create Table Name:= lower(Model Name)    
    type: str = "vendor"  
    name: str = Field(index=False)      
    description: str = Field(index=False)      
    email: EmailStr = Field(default=None)
    address: str = Field(default=None)
    products: List["Product"] = Relationship(back_populates="vendor")

    
    def validate(self) -> None:
        super().validate()
        if not self.email:
            raise ValueError("Email cannot be empty")
        
from sbox1.backend.models.product import Product  # At the bottom of vendor.py
