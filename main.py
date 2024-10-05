from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from backend.db.db_init import init_db, get_db
from backend.middlewares.request_logger import RequestLoggingMiddleware
from backend.controllers.vendors_controller import router as vendors_router
from fastapi.templating import Jinja2Templates
from backend.models.vendor import Vendor
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="/home/dp/Documents/appRAD/sbox1/backend/templates")

app = FastAPI()
app.add_middleware(RequestLoggingMiddleware, is_request_logging_on=False)
app.include_router(vendors_router, tags=["vendors"])
app.mount("/static", StaticFiles(directory="/home/dp/Documents/appRAD/sbox1/backend/static"), name="static")

@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def read_root():
    return {"Hello": "World"}
if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8081)

@app.get("/vendors/main")
async def list_vendors(request: Request
			, db: Session = Depends(get_db)
		):
    models = db.exec(select(Vendor)).all()
    # return print(vendors)
    return templates.TemplateResponse("vendors/list.j2"
		    , {"request": request, "models": models})