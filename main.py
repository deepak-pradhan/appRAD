import os
import logging
from pathlib import Path
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
from backend.controllers.ollama_controller import router as ollama_routes
from backend.controllers.model_file_controller import router as model_file_routes
from backend.controllers.llama_controller import router as llama_router

# Pre-Prep
current_dir = Path(__file__).parent
static_dir : str = current_dir / "backend" / "static"
templates_dir : str = f"{current_dir}/backend/templates"

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start
app = FastAPI(
    debug=os.getenv("DEBUG", True).lower() == "true"
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

# Load middlewares
app.add_middleware(RequestLoggerMiddleware
    , is_request_logging_on=True
)
app.add_middleware(CrumbMiddleware) # Pages in pages/*
app.add_middleware(
    CORSMiddleware,
    # allow_origins=os.getenv('ALLOW_ORIGINS', '').split(','),
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# mount View for Pages (HTMX + Jinja + MindJS + Alpine.js)
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(ollama_routes, tags=["ollama"])
app.include_router(model_file_routes, tags=["models"])
app.include_router(llama_router, prefix="/llama", tags=["llama"])

# @TODO: End points for Pages
@app.get("/")
def read_root(request: Request):    
    return templates.TemplateResponse("index.j2", {
        'request': request
        , 'name' : 'Joe'
    })
  
    
if __name__ == "__main__":
    import uvicorn 
    # uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8082)))