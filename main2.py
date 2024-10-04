from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from tenant import Base, Tenant, metadata
from typing import List
import json
from datetime import datetime
from sqlalchemy.orm import Session

app = FastAPI()

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Custom JSON encoder to handle datetime objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Helper function for input validation
def validate_tenant_data(data: dict, update: bool = False):
    if not update and ('name' not in data or 'email' not in data):
        raise HTTPException(status_code=400, detail="Name and email are required")
    if 'name' in data and (not isinstance(data['name'], str) or len(data['name']) > 100):
        raise HTTPException(status_code=400, detail="Invalid name")
    if 'email' in data and (not isinstance(data['email'], str) or len(data['email']) > 100):
        raise HTTPException(status_code=400, detail="Invalid email")

# CRUD Routes

@app.post("/tenants/", response_model=dict)
async def create_tenant(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    validate_tenant_data(data)
    db_tenant = Tenant(**data)
    try:
        db.add(db_tenant)
        db.commit()
        db.refresh(db_tenant)
        return json.loads(json.dumps(db_tenant.to_dict(), cls=CustomJSONEncoder))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

@app.get("/tenants/", response_model=List[dict])
def read_tenants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tenants = db.query(Tenant).offset(skip).limit(limit).all()
    return json.loads(json.dumps([tenant.to_dict() for tenant in tenants], cls=CustomJSONEncoder))

@app.get("/tenants/{tenant_id}", response_model=dict)
def read_tenant(tenant_id: int, db: Session = Depends(get_db)):
    db_tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return json.loads(json.dumps(db_tenant.to_dict(), cls=CustomJSONEncoder))

@app.put("/tenants/{tenant_id}", response_model=dict)
async def update_tenant(tenant_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    validate_tenant_data(data, update=True)
    db_tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    for key, value in data.items():
        setattr(db_tenant, key, value)
    
    try:
        db.commit()
        db.refresh(db_tenant)
        return json.loads(json.dumps(db_tenant.to_dict(), cls=CustomJSONEncoder))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

@app.delete("/tenants/{tenant_id}", response_model=dict)
def delete_tenant(tenant_id: int, db: Session = Depends(get_db)):
    db_tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    db.delete(db_tenant)
    db.commit()
    return {"message": "Tenant deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)