
import importlib
import logging
import os
from typing import List
from fastapi import Depends, HTTPException
from sqlmodel import Session

from backend.controllers.bases.bcontroller import BController
from backend.db.databases import get_db
from backend.models.bases.bmodel import BModel 

class FileController(BController):
    def __init__(self):
        super().__init__(model=BModel, resource_name="files")
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/models", self.list_models, methods=["GET"], response_model=List[str])
        self.router.add_api_route("/models/{model_name}", self.select_model, methods=["GET"], response_model=dict)


    async def list_models(self, db: Session = Depends(get_db)) -> List[str]:
        """
        List available models in the backend.models.* directory.
        In the future, this could be expanded to read from a database or file.
        """
        models_dir = os.path.dirname(os.path.abspath(__file__)).replace('controllers', 'models')
        model_files = [f[:-3] for f in os.listdir(models_dir) if f.endswith('.py') and f != '__init__.py']
        valid_models = []

        for model_file in model_files:
            module = importlib.import_module(f'backend.models.{model_file}')
            for name, obj in module.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, BModel) and obj != BModel:
                    valid_models.append(name)

        return valid_models

      


    async def select_model(self, model_name: str, db: Session = Depends(get_db)) -> dict:
        """
        Select a specific model and return its details.
        This could be expanded to load model details from a file or database.
        """
        # Placeholder implementation
        # TODO: Implement actual logic to select and return model details
        if model_name not in await self.list_models(db):
            raise HTTPException(status_code=404, detail="Model not found")
        return {"name": model_name, "attributes": ["attr1", "attr2"]}

    # Future methods for tracking generated models and saving templates
    async def save_template(self, template: dict, db: Session = Depends(get_db)):
        """
        Save a template for reuse by the synthetic data generator.
        """
        # TODO: Implement logic to save template
        pass

    async def get_generated_models(self, db: Session = Depends(get_db)) -> List[dict]:
        """
        Retrieve a list of generated models.
        """
        # TODO: Implement logic to retrieve generated models
        pass

file_controller = FileController()
router = file_controller.router

