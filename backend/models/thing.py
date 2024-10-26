from sqlmodel import Field
from backend.models.bases.bmodel import BModel
from abc import ABC, abstractmethod

class Thing(BModel, table=False):
    '''
    Products & Servces consume Materials
    Materials has origin(Plants, Animals, Humans, Natural)
    '''
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
    services: str  
    replaces: str
    replacer: str

    @abstractmethod
    def validate(self) -> None:
        """Custom validation """
        pass