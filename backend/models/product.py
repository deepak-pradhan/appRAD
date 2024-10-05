from sqlmodel import Field
from backend.models.base import CModel

class Product(CModel, table=True):
    __tablename__ = "product"
    type: str = "product"  
    name: str = Field(index=True)          
    vendor_id: int
    price : float 
    
    def validate(self) -> None:
        """Custom validation for the Tenant model"""
        if not self.name:
            raise ValueError("Name cannot be empty")
        if not self.name or not self.description:
            raise ValueError("Email cannot be empty")
