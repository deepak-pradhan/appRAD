from typing import Type, Any, Dict

from pathlib import Path

from fastapi import Depends, APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, func, select

from backend.db.databases import get_db
from backend.models.base import CModel
from backend.utils.pagination import Pagination
from backend.utils.filtering import apply_filters
from backend.utils.sorting import apply_sorting

# FS: Keep this import for FastUI
# from fastui import FastUI, AnyComponent, prebuilt_html, components as c
# from fastui.components.display import DisplayMode, DisplayLookup
# from fastui.events import GoToEvent, BackEvent

class BaseController:
    _current_dir: Path = Path(__file__).parent.parent.parent
    _templates_dir: str = str(_current_dir.joinpath("backend", "templates")) # default templates directory

    def __init__(self, model: Type[CModel], resource_name: str = None, templates_dir: str = None):
        self.model = model
        self.templates_dir = templates_dir or self._templates_dir  # Use the default templates_dir or override

        if resource_name is None:
            self.resource_name = self.model.__name__.lower() + 's'
        else:
            self.resource_name = resource_name

        self.templates = Jinja2Templates(directory=str(self.templates_dir))        
        self.router = APIRouter()

    def separate_headers_and_data(self, models):
        if not models:
            return [],[]
        
        model_class= type(models[0])

        # Get the column headers
        headers = [field.name for field in model_class.__table__.columns]
        
        # Extract data rows
        data_rows = []
        for instance in models:
            row = [getattr(instance, field) for field in headers]
            data_rows.append(row)
        
        return headers, data_rows

    # Create
    async def create(self, request: Request, db: Session = Depends(get_db)):
        ''' Create a new item '''
        data = await request.json()
        model = self.model.from_dict(data)
        model.validate() # add validation, untested! 
        db.add(model)
        db.commit()
        db.refresh(model)
        return
    async def create_batch(self, request: Request, db: Session = Depends(get_db)):
        ''' Create a new items '''
        data = await request.json()
        models = [self.model.from_dict(item) for item in data]
        self.model.bulk_create(db, models)
        return
    
    # Read
    async def read(self, request: Request, id: int, db: Session = Depends(get_db)):
        model = db.get(self.model, id)
        if model is None:
            return JSONResponse(status_code=404, content={"detail": "Item not found"})
        return model
    
    async def read_all(self, request: Request, db: Session = Depends(get_db)):
        models = db.exec(select(self.model)).all()
        return models
        
    async def list(self
            , request: Request
            , db: Session = Depends(get_db)
            , pagination: Pagination = Depends()
            , filters: Dict[str, Any] = None
            , sort: str = None
        ) -> HTMLResponse:
        
        pagination = Pagination(
            request=Request
            , page=pagination.page
            , page_size=pagination.page_size
        )
        offset = (pagination.page - 1) * pagination.page_size
        
        query = select(self.model)
        if filters:
            query = apply_filters(query, filters)
        
        if sort:
            query = apply_sorting(query, sort)
        
        models = db.exec(
            query
            .offset(offset)
            .limit(pagination.page_size)
        ).all()

        # if not models:
        #     self.logger.info(f"Info: No items in list method")
        #     return JSONResponse(status_code=404, content={"detail": "Item not found"})
       
        total = db.exec(select(func.count(self.model.id))).first()
        return models
    
        # @TODO: backend model admin         
        # headers, data = self.separate_headers_and_data(models)
        # return self.templates.TemplateResponse(
        #         "vendors/list.j2", {
        #                 "request": request
        #                 , "models": models
        #                 # , "headers": headers
        #                 # , "data": data
        #                 , "pagination": pagination
        #                 , "total": total
        #             }   
        #     )
        
    # Update
    async def update(self, request: Request, id: int, db: Session = Depends(get_db)):
        data = await request.json()
        model = db.get(self.model, id)
        if model is None:
            return JSONResponse(status_code=404, content={"detail": "Item not found"})
        
    # Delete v1    

    async def delete(self, request: Request, id: int, db: Session = Depends(get_db)):
        model = db.get(self.model, id)
        if model is None:
            return JSONResponse(status_code=404, content={"detail": "Item not found"})
        
        db.delete(model)
        db.commit()
        return JSONResponse(content={"detail": "Deleted successfully"})        
    
    async def toggle_active(self, id: int, db: Session = Depends(get_db)):
        model = db.get(self.model, id)
        if model is None:
            return JSONResponse(status_code=404, content={"detail": "Item not found"})
        model.is_active = not model.is_active
        db.add(model)
        db.commit()
        return {"status": "success", "is_active": model.is_active}
