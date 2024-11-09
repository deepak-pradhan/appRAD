# backend/controllers/flow_controller.py
from fastapi import APIRouter
from tinydb import TinyDB
from datetime import datetime

router = APIRouter()
db = TinyDB('flows.json')
flows_table = db.table('flows')

@router.post("/flows")
async def save_flow(flow_data: dict):
    flow_data["timestamp"] = datetime.now().isoformat()
    flows_table.insert(flow_data)
    return {"message": "Flow saved!", "flow_id": flow_data.get("id")}