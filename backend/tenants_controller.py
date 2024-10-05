import logging
from fastapi import Request, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy import func
from sqlmodel import Session, select
from models.tenant import Tenant
from controllers.base_controller import BaseController
from sqlalchemy.exc import IntegrityError
from utils.pagination import Pagination
from datetime import datetime, timedelta
from db.databases import get_db

class vendorsController(BaseController):
    def __init__(self):
        super().__init__(Tenant, "vendors")
        self.register_additional_routes()
        self.logger = logging.getLogger(__name__)


    def register_additional_routes(self):
        self.router.add_api_route("/vendors", self.list, methods=["GET"], name="list_vendors")
        self.router.add_api_route("/vendors", self.create, methods=["POST"], name="create_tenant")
        self.router.add_api_route("/vendors/new", self.new_tenant_form, methods=["GET"], name="new_tenant_form")
        self.router.add_api_route("/vendors/{id}", self.read, methods=["GET"], name="read_tenant")
        self.router.add_api_route("/vendors/{id}/edit", self.edit_form, methods=["GET"], name="edit_tenant_form")
        self.router.add_api_route("/vendors/{id}", self.update, methods=["POST"], name="update_tenant")
        self.router.add_api_route("/vendors/{id}", self.delete, methods=["DELETE"], name="delete_tenant")
        self.router.add_api_route("/vendors/{id}/toggle-active", self.toggle_active, methods=["PUT"], name="toggle_tenant_active")
        self.router.add_api_route("/vendors/{id}/generate_api_key", self.generate_api_key, methods=["POST"])
        self.router.add_api_route("/vendors/{id}/update_subscription", self.update_subscription, methods=["POST"])
        self.router.add_api_route("/vendors/{id}/subscription_status", self.get_subscription_status, methods=["GET"])
        self.router.add_api_route("/vendors/{id}/update_last_login", self.update_last_login, methods=["POST"])


    async def create(self, request: Request, db: Session = Depends(get_db)):
        form_data = await request.form()
        try:
            tenant = Tenant(**form_data)
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
            return RedirectResponse(url="/vendors", status_code=303)
        except IntegrityError as e:
            db.rollback()
            if "UNIQUE constraint failed: tenant.domain" in str(e):
                return self.templates.TemplateResponse(
                    "vendors/new.j2",
                    {"request": request, "error": "A tenant with this domain already exists"},
                    status_code=400
                )
            raise HTTPException(status_code=500, detail="An error occurred while creating the tenant")

    async def new_tenant_form(self, request: Request):
        return self.templates.TemplateResponse("vendors/new.j2", {"request": request})


   
    async def list(self
            , request: Request
            , db: Session = Depends(get_db)
            , pagination: Pagination = Depends()
            , page: int = 25):
        pagination = Pagination(request=Request, page=pagination.page, page_size=10)
        try:
            offset = (pagination.page - 1) * pagination.page_size
            query = select(Tenant)
            vendors = db.exec(query.offset(offset).limit(10)).all()
            total = db.exec(select(func.count(Tenant.id))).first()
            return self.templates.TemplateResponse(
                "vendors/list.j2",
                {"request": request, "vendors": vendors, "pagination": pagination, "total": total}
            )
        except Exception as e:
            self.logger.error(f"Error in tenant list method: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
        
    # async def list(self, request: Request, db: Session = Depends(get_db), pagination: Pagination = Depends()): 
    #     try:
    #         offset = (pagination.page - 1) * pagination.page_size
    #         query = select(Tenant)
    #         vendors = db.exec(query.offset(offset).limit(pagination.page_size)).all()
    #         total = db.exec(select(func.count(Tenant.id))).first() # [0]  # Updated this line
    #         return self.templates.TemplateResponse(
    #             "vendors/list.j2",
    #             {"request": request, "vendors": vendors, "pagination": pagination, "total": total}
    #         )
    #     except Exception as e:
    #         self.logger.error(f"Error in tenant list method: {str(e)}")
    #         raise HTTPException(status_code=500, detail="Internal server error")        
        
    async def read(self, request: Request, id: int, db: Session = Depends(get_db)):
        tenant = db.get(Tenant, id)
        if tenant is None:
            raise HTTPException(status_code=404, detail="Tenant not found")
        return self.templates.TemplateResponse("vendors/show.j2", {"request": request, "tenant": tenant})
    
    async def edit_form(self, request: Request, id: int, db: Session = Depends(get_db)):
        self.logger.debug(f"Attempting to edit tenant with id: {id}")
        tenant = db.get(Tenant, id)
        if tenant is None:
            self.logger.warning(f"Tenant with id {id} not found for editing")
            raise HTTPException(status_code=404, detail="Tenant not found")
        self.logger.debug(f"Successfully retrieved tenant for editing: {tenant.name}")
        return self.templates.TemplateResponse("vendors/edit.j2", {"request": request, "tenant": tenant})

    async def update(self, request: Request, id: int, db: Session = Depends(get_db)):
        form_data = await request.form()
        tenant = db.get(Tenant, id)
        if tenant is None:
            raise HTTPException(status_code=404, detail="Tenant not found")
        for key, value in form_data.items():
            if key == 'is_active':
                value = value.lower() == 'on'
            setattr(tenant, key, value)
        db.add(tenant)
        db.commit()
        db.refresh(tenant)

    async def delete(self, request: Request, id: int, db: Session = Depends(get_db)):
        tenant = db.get(Tenant, id)
        if tenant is None:
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        db.delete(tenant)
        db.commit()
        return JSONResponse(content={"detail": "Tenant deleted successfully"})
    
    
    async def toggle_active(self, id: int, db: Session = Depends(get_db)):
        tenant = db.get(Tenant, id)
        if tenant is None:
            raise HTTPException(status_code=404, detail="Tenant not found")
        tenant.is_active = not tenant.is_active
        db.add(tenant)
        db.commit()
        return {"status": "success", "is_active": tenant.is_active}

    async def generate_api_key(self, request: Request, id: int, db: Session = Depends(get_db)):
        tenant = db.get(Tenant, id)
        if tenant is None:
            raise HTTPException(status_code=404, detail="Tenant not found")
        tenant.generate_api_key()
        db.add(tenant)
        db.commit()
        return JSONResponse(content={"api_key": tenant.api_key})

    async def update_subscription(self, request: Request, id: int, db: Session = Depends(get_db)):
        form_data = await request.form()
        tenant = db.get(Tenant, id)
        if tenant is None:
            raise HTTPException(status_code=404, detail="Tenant not found")
        new_plan = form_data.get("subscription_plan")
        duration_days = int(form_data.get("duration_days", 30))
        end_date = datetime.now() + timedelta(days=duration_days)
        tenant.update_subscription(new_plan, end_date)
        db.add(tenant)
        db.commit()
        return JSONResponse(content=tenant.to_dict())

    async def get_subscription_status(self, request: Request, id: int, db: Session = Depends(get_db)):
        tenant = db.get(Tenant, id)
        if tenant is None:
            raise HTTPException(status_code=404, detail="Tenant not found")
        return JSONResponse(content={
            "is_active": tenant.is_subscription_active(),
            "days_until_expiry": tenant.days_until_subscription_expires(),
            "plan": tenant.subscription_plan
        })

    async def update_last_login(self, request: Request, id: int, db: Session = Depends(get_db)):
        tenant = db.get(Tenant, id)
        if tenant is None:
            raise HTTPException(status_code=404, detail="Tenant not found")
        tenant.update_last_login()
        db.add(tenant)
        db.commit()
        return JSONResponse(content={"detail": "Last login updated successfully"})

vendors_controller = vendorsController()
router = vendors_controller.router