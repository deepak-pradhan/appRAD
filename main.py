from fastapi import FastAPI, Request, Depends
from sqlmodel import Session, select
from backend.db.db_init import init_db, get_db
from backend.middlewares.request_logger import RequestLoggingMiddleware
from backend.middlewares.breadcrumb import BreadcrumbMiddleware
from fastapi.templating import Jinja2Templates
from backend.models.vendor import Vendor
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    if request.headers.get("accept") == "text/html":
        return templates.TemplateResponse("vendors/list.j2"
		    , {"request": request, "models": models}
        )
    
    return models

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8081)


# INFO:     Uvicorn running on http://0.0.0.0:8081 (Press CTRL+C to quit)
# INFO:root:Incoming request: GET http://127.0.0.1:8081/vendors
# INFO:root:Request headers: 
#     Headers(
#         {'host': '127.0.0.1:8081'
#          , 'connection': 'keep-alive'
#          , 'cache-control': 'max-age=0'
#          , 'sec-ch-ua': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"'
#          , 'sec-ch-ua-mobile': '?0'
#          , 'sec-ch-ua-platform': '"Linux"'
#          , 'upgrade-insecure-requests': '1'
#          , 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
#          , 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
#          , 'sec-gpc': '1'
#          , 'accept-language': 'en-US,en'
#          , 'sec-fetch-site': 'none'
#          , 'sec-fetch-mode': 'navigate'
#          , 'sec-fetch-user': '?1'
#          , 'sec-fetch-dest': 'document'
#          , 'accept-encoding': 'gzip, deflate, br, zstd'})
# INFO:     127.0.0.1:47408 - "GET /vendors HTTP/1.1" 200 OK

