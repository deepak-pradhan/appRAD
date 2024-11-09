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
    phone: str = Field(unique=True)
    rating: int = Field(default=0)

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
        structure[FIELDS_KEY][field_name] = {
            "type": str(field.annotation),
            "default": field.default
        }

    if hasattr(model_class, "__sqlmodel_relationships__"):
        for rel_name, rel in model_class.__sqlmodel_relationships__.items():
            relationship_info = {TYPE_KEY: "relationship"}
            if rel.sa_relationship:
                relationship_info[MODEL_KEY] = rel.sa_relationship.argument.__name__ if rel.sa_relationship.argument else "Unknown"
                relationship_info[BACK_POPULATES_KEY] = rel.sa_relationship.back_populates
            structure[RELATIONSHIPS_KEY][rel_name] = relationship_info

    return structure
def create_prompt(model_class: type[SQLModel]) -> str:
    structure = get_model_structure(model_class)
    prompt = f"Create a python class for the following model:\n\n"
    return structure

structure = create_prompt(Book)
from beeprint import pp
pp(structure)

