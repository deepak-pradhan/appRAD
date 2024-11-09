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
    # find_by_id (tid)    
    # find_by_aid (tid, aid)
    # find_by_aids (tid)
    # find_by_cid (tid, aid, cid)
    # find_by_cids (tid, aid)
    # find_is_keeps(x=True, y=False)  
    # find_is_keeps(x=False, y=True)  
    # find_is_keeps(x=True, y=True)  
        
    ## Update
    # self.is (type, name, description) # define things
    # self.state (tid, aid, cid, state)
    # self.is_keep_x (tid, aid, cid, is_keep)
    # self.is_keep_y (tid, aid, cid, is_keep)
    # self.is_final (tid, aid, cid, is_keep)

    # h1 & hM
    # self.action (tid, aid, cid, has_one = {tid, aid})
    # self.actions (tid, aid, cid, has_many = [[tid, aid, cid],...])    
    # self.action_context (tid, aid, cid, is_keep)
    # self.action_contexts (tid, aid, cid, is_keep)

        
    # Delete    
    
    async def toggle_state(self, id: int, db: Session = Depends(get_json)):
        pass
    