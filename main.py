from fastapi import FastAPI, Request, Depends
from sqlmodel import Session, select
from backend.db.db_init import init_db, get_db
from backend.middlewares.request_logger import RequestLoggingMiddleware
from backend.middlewares.breadcrumb import BreadcrumbMiddleware
from fastapi.templating import Jinja2Templates
from backend.models.vendor import Vendor
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Pre-Prep
current_dir = Path(__file__).parent
static_dir : str = current_dir / "backend" / "static"
templates_dir : str = current_dir / "backend" / "templates"

# Start
app = FastAPI()

# Prep
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

app.add_middleware(RequestLoggingMiddleware, is_request_logging_on=False)
app.add_middleware(BreadcrumbMiddleware)

@app.on_event("startup")
def on_startup():
    init_db()

# End points
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.j2", {
        'request': request
        , 'name' : 'Joe'
    })

@app.get("/vendors")
async def list(request: Request
			, db: Session = Depends(get_db)
		):    
    models = db.exec(select(Vendor)).all()
    return templates.TemplateResponse("vendors/list.j2"
		    , {"request": request, "models": models}
    )

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8081)
