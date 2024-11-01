from datetime import datetime
from typing import Dict, Any, Union
from sqlalchemy.sql.type_api import TypeEngine
from sqlmodel import SQLModel, Field, Relationship, ForeignKey, create_engine
from typing import List
from beeprint import pp
import json

engine = create_engine("sqlite:///tgen.db")
SQLModel.metadata.create_all(engine)

class Author(SQLModel, extend_existing=True):
    id: int = Field(default=1, primary_key=True)
    name: str = Field(index=True, description='Name of author')
    phone: str = Field(unique=True, max_length=15, description='Phone number of author')
    rating: int = Field(default=None, min_length=0, max_length=5)

class Book(SQLModel, extend_existing=True):
    id: int = Field(default=1, primary_key=True)
    title: str = Field()
    price: float | None = None
    author_id: int = Field(foreign_key="author.id")
    author: "Author" = Relationship(back_populates="books")
    


from typing import Dict, Any

# Define constants at the module level
FIELDS_KEY = "fields"
RELATIONSHIPS_KEY = "relationships"
TYPE_KEY = "type"
TARGET_KEY = "target"
MODEL_KEY = "model"
BACK_POPULATES_KEY = "back_populates"

def get_model_structure(model_class: type[SQLModel]) -> Dict[str, Any]:
    structure = {
        FIELDS_KEY: {},
        RELATIONSHIPS_KEY: {}
    }

    for field_name, field in model_class.__fields__.items():
        field_info = {
            "type": str(field.annotation),
            "default": field.default,
            "required": field.is_required,
            "description": field.description,
            "constraints": {},
            "metadata": {}
        }
        
        # Add constraints
        if hasattr(field, 'max_length'):
            field_info["constraints"]["max_length"] = field.field_info.max_length
        if hasattr(field, 'gt'):
            field_info["constraints"]["gt"] = field.field_info.gt
        if hasattr(field, 'lt'):
            field_info["constraints"]["lt"] = field.field_info.lt

        # Add metadata
        if field.index:
            field_info["metadata"]["index"] = True
        if field.unique:
            field_info["metadata"]["unique"] = True
        
        # Add validators
        if hasattr(field, 'validators'):
            field_info["validators"] = [v.__name__ for v in field.validators]

        structure[FIELDS_KEY][field_name] = field_info

    if hasattr(model_class, "__sqlmodel_relationships__"):
        for rel_name, rel in model_class.__sqlmodel_relationships__.items():
            relationship_info = {
                TYPE_KEY: "relationship",
                "cardinality": "one-to-many" if rel.sa_relationship.uselist else "one-to-one",
                MODEL_KEY: rel.sa_relationship.argument.__name__ if rel.sa_relationship.argument else "Unknown",
                BACK_POPULATES_KEY: rel.sa_relationship.back_populates
            }
            structure[RELATIONSHIPS_KEY][rel_name] = relationship_info

    return structure
def create_prompt(model_class: type[SQLModel]) -> str:
    structure = get_model_structure(model_class)
    prompt = f"Create a python class for the following model:\n\n"
    return structure

structure = create_prompt(Author)
from beeprint import pp
pp(structure)

