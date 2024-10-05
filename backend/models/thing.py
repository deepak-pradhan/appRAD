from sqlmodel import Field
from backend.models.base import CModel
from abc import ABC, abstractmethod

class Thing(ABC, CModel, table=True):
    __tablename__ = "thing"
    alternate_name : str = Field(default=None) 
    additional_types: str = Field(default=None)
    image: str = Field(default=None)
    disambiguating_description: str = Field(default=None)
    # instance properties
    about : str
    category: str
    knows_About : str
    mentions: str
    produces: str
    replaces: str
    replacer: str
    services: str  

    @abstractmethod
    def validate(self) -> None:
        """Custom validation """
        pass