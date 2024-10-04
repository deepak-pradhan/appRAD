import logging
from fastapi import FastAPI, Response
from sqlalchemy import create_engine
from tenant import Tenant
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.INFO)  

def get_db():
    db = Session(create_engine("sqlite:///example.db"))
    try:
        yield db
    finally:
        db.close()

app = FastAPI()


@app.get("/")
async def index(db: Session):
    tenants = Tenant.all(db)
    return {"message": f"Tenant {tenants}"}

@app.get("/tenant/{id}")
def get_tenant(id: int, db: Session):
    tenant = db.query(Tenant).get(id)
    if tenant:
        return {"message": f"Tenant {tenant.name} found"}
    else:
        return Response(status_code=404)

@app.post("/tenant")
async def create_tenant(name: str, email: str):
    session = Session(create_engine("sqlite:///example.db"))
    db = await session.get_session()
    tenant = Tenant(name=name, email=email)
    await tenant.save(db)

@app.put("/tenant/{id}")
async def update_tenant(id: int, name: str, email: str):
    session = Session(create_engine("sqlite:///example.db"))
    db = await session.get_session()
    tenant = await Tenant.get(id, db)
    if tenant:
        tenant.name = name
        tenant.email = email
        await tenant.save(db)
    else:
        return Response(status_code=404)

@app.delete("/tenant/{id}")
async def delete_tenant(id: int):
    session = Session(create_engine("sqlite:///example.db"))
    db = await session.get_session()
    tenant = await Tenant.get(id, db)
    if tenant:
        await tenant.delete(db)
    else:
        return Response(status_code=404)

# Create some sample data
async def create_sample_data():
    session = Session(create_engine("sqlite:///example.db"))
    db = await session.get_session()
    tenant1 = Tenant(name="John Doe 1", email="john.doe1@example.com")
    tenant2 = Tenant(name="Jane Doe 2", email="jane.doe2@example.com")
    await tenant1.save(db)
    await tenant2.save(db)


# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)