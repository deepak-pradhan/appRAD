from typing import Type

from pathlib import Path

from fastapi import Depends, APIRouter, Request
from fastapi.templating import Jinja2Templates

from backend.db.databases import get_json
from backend.models.bases.bmodel import CModel

class CController:
    _current_dir: Path = Path(__file__).parent.parent.parent
    _templates_dir: str = str(_current_dir.joinpath("backend", "templates")) # default templates directory

    def __init__(self, model: Type[CModel], resource_name: str = None, templates_dir: str = None):
        self.model = model
        self.templates_dir = templates_dir # No override for in-processs context templates

        if resource_name is None:
            resource_name = self.model.__name__.lower() + 's'

        self.resource_name = resource_name
        self.templates = Jinja2Templates(directory=str(self.templates_dir))        
        self.router = APIRouter()


    # Create
    async def create(self, request: Request, db: Session = Depends(get_json)):
        pass

    
    # Read
    async def read(self, request: Request, id: int, db: Session = Depends(get_json)):
        pass
    # find_by_id    
    # find_by_aid
    # find_by_cid

        
    # Update
        
    # Delete    
    
    async def toggle_state(self, id: int, db: Session = Depends(get_json)):
        pass
    