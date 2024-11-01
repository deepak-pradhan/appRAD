import secrets
from typing import Any, Dict, Optional, List
from sqlmodel import Column, Field, Session, select, Relationship, Enum
from pydantic import EmailStr
# from enum import Enum
from datetime import date

from backend.db.databases import get_db
from backend.models.bases.bmodel import BModel
# from backend.models.postal_address import PostalAddress

class Location:
    pass

class OrganizationType(str, Enum):
    '''
    This is an empty docstring for the Organization class. 
    It should be used to provide a brief description of the purpose and functionality of the Organization class.
    '''
    SOLE_PROPRIETORSHIP = "Sole Proprietorship"
    PARTNERSHIP = "Partnership"
    LIMITED_LIABILITY_COMPANY = "LLC"
    CORPORATION = "Corporation"
    NON_PROFIT = "Non-Profit"
    GOVERNMENT = "Government"
    OTHER = "Other"
    # org_type = OrganizationType.CORPORATION


class Organization(BModel, table=True):
    __tablename__ = "organization"
    rec_type: str = Field(default="Organization")
    # type: OrganizationType = Column(Enum(OrganizationType), nullable=True) 

    # Core properties
    legal_name: str = Field(index=True,min_length=5, max_length=80, description="Registered company name") 
    alternate_name: str | None = Field(default=None, max_length=80, description="an alias for the item, DBA")
    description: str | None = None
    duns: str | None = None
    url: str | None = None
    logo: str | None = Field(default=None, description="Type: ImageObject or URL")

    # Address relationship
    address_id: int | None = Field(default=None, foreign_key="postal_address.id")
    # address: PostalAddress = Relationship()

    # Contact properties
    contact_name: str | None = Field(default=None, description="Primary contact: person.name")
    contact_email: EmailStr | None = None
    contact_telephone: str | None = None
    contact_fax_number: str | None = None

    # Additional properties
    number_of_employees: int | None = Field(default=None, min_length=1, description="Type: QuantitativeValue")
    founding_date: date | None = None
    dissolution_date: date | None = None
    founding_location: str | None = None
    is_ic_ann_report: bool | None = None
    lei_code: str | None = None
    naics: str | None = None
    tax_id: str | None = None
    vat_id: str | None = None
    global_location_number: str | None = None  # GLN or ILN
    is_family_friendly: bool | None = None
    knows_languages: str | None = None # indicate a known language.
    keywords: str | None = None
    # member_of: str | None = Field(default=None)  
    number_of_locations: int | None = None
    slogan: str | None = None
    email: EmailStr | None = None
    legal_type: str | None = None
    hq_location: Location = Relationship()
    
    ## has Many
    # awards: Awards = Relationship()
    # departments
    # employees
    # events
    # fax_numbers
    # founders
    # offer_catalogs
    # Place - Points-of-Sales
    # makes_offer: str | None = Field(default=None)  # Expected type: Offer - A pointer to products or services offered by the organization or person.
    
    member: str | None = Field(default=None)  # Expected type: Organization or Person - A member of an Organization or a ProgramMembership.
    owns: str | None = Field(default=None)  # Expected type: OwnershipInfo or Product - Products owned by the organization or person.
    parent_organization: str | None = Field(default=None)  # Expected type: Organization - The larger organization that this organization is a subOrganization of, if any.
    # publishing_principles: str | None = Field(default=None)  # Expected type: CreativeWork or URL - The publishingPrinciples property indicates a document describing the editorial principles of an Organization.
    review: str | None = Field(default=None)  # Expected type: Review - A review of the item.
    # seeks: str | None = Field(default=None)  # Expected type: Demand - A pointer to products or services sought by the organization or person.
    # sponsor: str | None = Field(default=None)  # Expected type: Organization or Person - A person or organization that supports a thing through a pledge, promise, or financial contribution.
    sub_organization: str | None = Field(default=None)  # Expected type: Organization - A relationship between two organizations where the first includes the second, e.g., as a subsidiary.
    telephone: str | None = Field(default=None)  # Expected type: Text - The telephone number.
    # unnamedources_policy: str | None = Field(default=None)  # Expected type: CreativeWork or URL - For an Organization (typically a NewsMediaOrganization), a statement about policy on use of unnamed sources and the decision process required.
    # brand: str | None = Field(default=None)  # Expected type: Brand or Organization - The brand(s) associated with a product or service, or the brand(s) maintained by an organization or business person.

    def validate(self) -> None:
        super().validate()
        if not self.legal_name:
            raise ValueError("Legal name is required for an organization")

    @property
    def display_name(self) -> str:
        return self.alternate_name or self.legal_name

    @classmethod
    def get_by_name(cls, session: Session, name: str) -> Optional['Organization']:
        return session.exec(select(cls).where(cls.legal_name == name)).first()

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        return data

    @classmethod
    def get_active_organizations(cls) -> List['Organization']:
        with Session(get_db) as session:
            return session.exec(select(cls).where(cls.is_active == True)).all()
        
    @staticmethod
    def generate_unique_identifier() -> str:
        return secrets.token_urlsafe(16)

    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.legal_name}')>"