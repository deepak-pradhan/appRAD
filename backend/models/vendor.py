from sqlmodel import Field
from pydantic import EmailStr
from backend.models.base import CModel

class Vendor(CModel, table=True):
    __tablename__ = "vendor"
    type: str = "vendor"  
    name: str = Field(index=False)          
    email: EmailStr = Field(default=None)
    
    def validate(self) -> None:
        """Custom validation for the Tenant model"""
        if not self.name:
            raise ValueError("Name cannot be empty")
        if not self.email:
            raise ValueError("Email cannot be empty")
