import logging
from typing import Any, Dict

from fastapi.responses import JSONResponse
from backend.models.vendor import Vendor
from backend.controllers.base_controller import BaseController
from backend.db.databases import get_db
from backend.utils.filtering import apply_filters
from backend.utils.sorting import apply_sorting

from fastapi import Depends, HTTPException, Request
from sqlmodel import Session, func, select
from backend.utils.pagination import Pagination

class vendorsController(BaseController):
    def __init__(self):
        super().__init__(Vendor, "vendors")
        self.register_additional_routes()
        self.logger = logging.getLogger(__name__)


    def register_additional_routes(self):
        pass
        self.router.add_api_route("/vendors", self.list, methods=["GET"], name="list")
        # self.router.add_api_route("/vendors", self.create, methods=["POST"], name="create")
        # self.router.add_api_route("/vendors/new", self.new_form, methods=["GET"], name="new_form")
        # self.router.add_api_route("/vendors/{id}", self.read, methods=["GET"], name="read")
        # self.router.add_api_route("/vendors/{id}/edit", self.edit_form, methods=["GET"], name="edit_form")
        # self.router.add_api_route("/vendors/{id}", self.update, methods=["POST"], name="update")
        # self.router.add_api_route("/vendors/{id}", self.delete, methods=["DELETE"], name="delete")
        # self.router.add_api_route("/vendors/{id}/toggle-active", self.toggle_active, methods=["PUT"], name="toggle_active")

    async def list(self
            , request: Request
            , db: Session = Depends(get_db)
            , pagination: Pagination = Depends()
            , filters: Dict[str, Any] = None
            , sort: str = None
        ):
        
        pagination = Pagination(
            request=Request
            , page=pagination.page
            , page_size=pagination.page_size
        )
        offset = (pagination.page - 1) * pagination.page_size
        
        query = select(Vendor)
        if filters:
            query = apply_filters(query, filters)
        
        if sort:
            query = apply_sorting(query, sort)
        
        models = db.exec(
            query
            .offset(offset)
            .limit(pagination.page_size)
        ).all()

        if not models:
            self.logger.info(f"Info: No items in list method")
            raise HTTPException(status_code=200, detail="No items found")
        
        total = db.exec(select(func.count(Vendor.id))).first()

        return self.templates.TemplateResponse(
                "vendors/list.j2", {
                        "request": request
                        , "models": models
                        , "pagination": pagination
                        , "total": total
                    }   
            )

vendors_controller = vendorsController()
router = vendors_controller.router