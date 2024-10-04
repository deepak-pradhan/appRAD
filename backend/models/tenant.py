import re
import secrets
from datetime import datetime, timezone
from typing import Any, Dict, Optional, List
from sqlmodel import Field, SQLModel, Session, select
from pydantic import EmailStr
from backend.models.base import CModel
from backend.db.databases import engine, get_db

class Tenant(CModel, table=True):
    __tablename__ = "tenants"
    rec_type: str = Field(default="tenant")  

    first_name: str = Field(index=True)                       # Tenant name, indexed for faster queries
    last_name: str = Field(index=True)                       # Tenant name, indexed for faster queries
    email: EmailStr = Field(default=None)       # Primary contact email for the tenant
    
    def validate(self) -> None:
        """Custom validation for the Tenant model"""
        if not self.first_name or not self.last_name:
            raise ValueError("Tenant name cannot be empty")
        if not self.email:
            raise ValueError("Email cannot be empty")

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
        data['is_subscription_active'] = self.is_subscription_active()
        data['days_until_expiry'] = self.days_until_subscription_expires()
        return data

    @classmethod
    def get_active_tenants(cls) -> List['Tenant']:
        with Session(get_db) as session:
            return session.exec(select(cls).where(cls.is_active == True)).all()
        
    @staticmethod
    def generate_unique_identifier() -> str:
        """Generate a unique identifier for the tenant"""
        return secrets.token_urlsafe(16)

    def generate_api_key(self):
        pass

    def __repr__(self):
        """String representation of the Tenant instance"""
        return f"<Tenant(id={self.id}, name='{self.get_by_name}')>"