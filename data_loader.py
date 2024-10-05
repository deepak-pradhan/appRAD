from fastapi import FastAPI
from backend.db.db_init import init_db
from backend.utils.load_data import load_data

app = FastAPI()
@app.on_event("startup")
def on_startup():
    init_db()
    load_data()
()
