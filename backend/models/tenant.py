import secrets
from typing import Any, Dict, Optional, List
from sqlmodel import Field, Session, select
from pydantic import EmailStr
from backend.db.databases import get_db
from backend.models.bases.bmodel import BModel

""" 
https://schema.org/Organization
"""

class Tenant(BModel, table=True):
    __tablename__ = "tenant"
    rec_type: str = Field(default="BE")  

    legal_name: str = Field(index=True, default='ACME Bagel Ltd.')
    post_office_box_number : str = Field(default=None)
    street_address: str = Field(default='Bagel Street 1234')
    postal_code: str = Field(default='12345')
    address_locality: str = Field(default='Munich Germany')
    address_region: str = Field(default=None)
    address_country: str = Field(default=None) 

    duns: str

    first_name: str = Field(index=True)          
    last_name: str = Field(index=True)           
    company_name: str = Field(default=None)      
    company_email: EmailStr = Field(default=None)
    personal_email: EmailStr = Field(default=None)      


    
    def validate(self) -> None:
        """Custom validation for the Tenant model"""
        pass

    @property
    def display_name(self) -> str:
        """Human-readable representation of the tenant"""
        return f"{self.first_name} ({self.last_name})"

    @classmethod
    def get_by_name(cls, session: Session, name: str) -> Optional['Tenant']:
        """Retrieve a tenant by its name"""
        return session.exec(select(cls).where(cls.first_name == name)).first()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the tenant to a dictionary, including derived fields"""
        data = super().to_dict()
        return data

    @classmethod
    def get_active_vendors(cls) -> List['Tenant']:
        with Session(get_db) as session:
            return session.exec(select(cls).where(cls.is_active == True)).all()
        
    @staticmethod
    def generate_unique_identifier() -> str:
        """Generate a unique identifier for the tenant"""
        return secrets.token_urlsafe(16)


    def __repr__(self):
        """String representation of the Tenant instance"""
        return f"<Tenant(id={self.id}, name='{self.get_by_name}')>"