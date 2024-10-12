import os
import logging
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from backend.db.db_init import init_db, get_db
from backend.middlewares.request_logger import RequestLoggerMiddleware
from backend.middlewares.crumb import CrumbMiddleware
from backend.models.vendor import Vendor
from backend.controllers.vendors_controller import router as vendors_routes
from backend.controllers.ollama_controller import router as ollama_routes
from backend.models.l_model import LModel

# Pre-Prep
current_dir = Path(__file__).parent
static_dir : str = current_dir / "backend" / "static"
templates_dir : str = f"{current_dir}/backend/templates"
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Start
app = FastAPI(
    debug=os.getenv("DEBUG", False).lower() == "true"
    )

@app.on_event("startup")
def on_startup():
    init_db()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please try again later."}
    )

# Prep
app.add_middleware(RequestLoggerMiddleware
    , is_request_logging_on=True
)
app.add_middleware(CrumbMiddleware)
app.add_middleware(
    CORSMiddleware,
    # allow_origins=os.getenv('ALLOW_ORIGINS', '').split(','),
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)
app.add_exception_handler(Exception, global_exception_handler)


app.include_router(vendors_routes, tags=["vendors"])
app.include_router(ollama_routes, tags=["ollama"])
# app.add_api_route("/chat", OllamaController.chat_with_ollama, methods=["POST"])


# End points
@app.get("/")
def read_root(request: Request):    
    return templates.TemplateResponse("index.j2", {
        'request': request
        , 'name' : 'Joe'
    })


@app.get("/vendors")
async def list_vendors( request: Request, db: Session = Depends(get_db)) :    
    models= db.exec(select(Vendor)).all()
    if request.headers.get("accept") == "text/html":
        return templates.TemplateResponse("vendors/list.j2", {
                "request": request, "models": models
        })
    
    return models
    
    
if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8081)))