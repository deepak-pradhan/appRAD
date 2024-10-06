from typing import Type
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from backend.models.base import CModel

class BaseController:
    def __init__(self, model: Type[CModel], resource_name: str):
        self.model = model
        self.resource_name = resource_name
        self.router = APIRouter()
        self.templates = Jinja2Templates(directory="/home/dp/Documents/appRAD/sbox1/backend/templates")