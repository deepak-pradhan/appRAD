from datetime import datetime, timezone
import logging

from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from sqlmodel import Session

from backend.db.databases import get_db
from backend.models.vendor import Vendor
from backend.controllers.bases.bcontroller import BController

class VendorsController(BController):
    def __init__(self):
        super().__init__(Vendor, "vendors")
        self.register_additional_routes()
        self.logger = logging.getLogger(__name__)


    def register_additional_routes(self):
        pass
        self.router.add_api_route(f"/{self.resource_name}", self.create, methods=["POST"], name="create")
        self.router.add_api_route(f"/{self.resource_name}", self.list, methods=["GET"], name="list")
        self.router.add_api_route(f"/{self.resource_name}/{{id}}", self.read, methods=["GET"], name="read")
        self.router.add_api_route(f"/{self.resource_name}/{{id}}", self.update, methods=["PUT"], name="update")
        self.router.add_api_route(f"/{self.resource_name}/{{id}}", self.delete, methods=["DELETE"], name="delete")
        # self.router.add_api_route("/vendors/{id}/toggle-active", self.toggle_active, methods=["PUT"], name="toggle_active")
        # self.router.add_api_route("/vendors/new", self.new_form, methods=["GET"], name="new_form")
        # self.router.add_api_route("/vendors/{id}/edit", self.edit_form, methods=["GET"], name="edit_form")

    async def create(self, request: Request, db: Session = Depends(get_db)):
        """
        Create a new vendor.

        Args:
            vendor (VendorCreate): The vendor data to create.
            db (Session): The database session.

        Returns:
            Vendor: The created vendor object.
        """
        form_data = await request.form()
        model_data = {key: value for key, value in form_data.items() if value}
        if 'name' not in model_data or not model_data['name']:
            return JSONResponse(status_code=400, content={"detail": "Name is required"})
        model = Vendor(**model_data)
        db.add(model)
        db.commit()
        db.refresh(model)
        return JSONResponse(status_code=200, content={"detail": "Item created"})

    
    async def update(self, id:int, db: Session = Depends(get_db), **kwargs):
        """Update the model instance with new values"""
        # body = await request.json()

        logging.info(f"Updating vendor with ID: {id}")
        logging.info(f"Received update data: {kwargs}")

        model = db.get(Vendor, id)
        if not model:
            logging.warning(f"Vendor with ID {id} not found")
            return JSONResponse(status_code=404, content={"detail": "Vendor not found"})

        for key, value in kwargs.items():
            if hasattr(model, key):
                logging.info(f"Updating field: {key} with value: {value}")
                setattr(model, key, value)
            else:
                logging.warning(f"Attempted to update non-existent field: {key}")

        model.updated_at = datetime.now(timezone.utc)
        db.add(model)
        db.commit()
        db.refresh(model)
        logging.info(f"Vendor {id} updated successfully")
        return model

vendors_controller = VendorsController()
router = vendors_controller.router
