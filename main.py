import logging
from fastapi import FastAPI
from backend.db.db_init import init_db
from backend.middlewares.request_logger import RequestLoggingMiddleware
from backend.utils.load_initals_data import load_sample_tenants



app = FastAPI()
app.add_middleware(RequestLoggingMiddleware, is_request_logging_on=False)

@app.on_event("startup")
def on_startup():
    init_db()
    load_sample_tenants()

@app.get("/")
def read_root():
    return {"Hello": "World"}
if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8081)