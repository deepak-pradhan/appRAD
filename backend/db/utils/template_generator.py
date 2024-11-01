import os
import re
import json
import requests
import importlib
from decimal import Decimal
from typing import List, Dict, Any, get_origin
from sqlmodel import SQLModel
from pydantic import EmailStr

class TemplateGenerator:
    def __init__(self, model_name: str = 'vendor.py', number_of_samples: int = 1):
        self.model_name = model_name
        self.number_of_samples = number_of_samples
        self.model = self.read_model()
        self.attributes = self.get_model_attributes()
        self.template = self.generate_template()
        self.prompt = self.generate_prompt()

    def read_model(self) -> SQLModel:
        model_name = self.model_name.replace('.py', '')
        model_path = f"backend.models.{model_name}"
        file_path = f"backend/models/{model_name}.py"
        
        if not os.path.exists(file_path):
            raise ValueError(f"Model file not found: {file_path}")
        
        try:
            module = importlib.import_module(model_path)
            model = getattr(module, model_name.capitalize())
            if not issubclass(model, SQLModel):
                raise ValueError(f"{model_name} is not a subclass of SQLModel")
            return model
        except AttributeError:
            raise ValueError(f"Model {model_name} not found in {model_path}")
    def get_model_attributes(self) -> List[str]:
        return [field for field in self.model.__fields__ if field not in ['id', 'created_at', 'updated_at', 'type']]
    def generate_template(self) -> Dict[str, Any]:
        template = {}
        for attr, field in self.model.__fields__.items():
            if attr not in ['id', 'created_at', 'updated_at', 'type']:
                if get_origin(field.annotation) is List:
                    template[attr] = []
                elif field.annotation == EmailStr:
                    template[attr] = "user@example.com"
                elif field.annotation == Decimal:
                    template[attr] = "0.00"
                elif field.annotation == bool:
                    template[attr] = False
                elif field.annotation == int:
                    template[attr] = 0
                else:
                    template[attr] = ""
        
        print(f"Generated template\n: {template}")
        return template    
    
    def generate_prompt(self) -> str:
        return f"Generate a unique and diverse synthetic sample data sets for {self.model_name}. Each data set should include values for these attributes: {', '.join(self.attributes)}. Use this template as a guide: {json.dumps(self.template)}. Ensure all generated data is generated to US address."


    def test_template(self, model: str = 'llama3.1:8b', temperature: float = 2.5, top_p: float = 0.99, top_k: int = 100) -> List[Dict[str, Any]]:
        data = {
            "prompt": self.prompt,
            "model": model,
            "format": "json",
            "stream": False,
            "options": {"temperature": temperature, "top_p": top_p, "top_k": top_k},
        }

        print("\nPrompt:",self.prompt)
        print("\n model", model)

        try:
            response = requests.post("http://localhost:11434/api/generate", json=data, stream=False)
            json_data = json.loads(response.text)
            print(f"Raw AI response:\n {json_data}")
        
            # Parse the JSON string from the 'response' field
            # generated_data = json.loads(json_data['response'])
        
            # Ensure generated_data is a list
            if not isinstance(json_data, list):
                generated_data = [json_data]
        
            self.validate_generated_data(generated_data)
            return generated_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except requests.RequestException as e:
            print(f"Error making request: {e}")
        except ValueError as e:
            print(f"Validation error: {e}")
        return []

    def validate_generated_data(self, data: List[Dict[str, Any]]) -> None:
        for item in data:
            try:
                self.model(**item)
            except ValueError as e:
                raise ValueError(f"Generated data does not match model schema: {e}")

    def save_assets(self, filename: str) -> None:
        assets = {
            "template": self.template,
            "prompt": self.prompt
        }
        with open(f"{filename}.json", "w") as f:
            json.dump(assets, f, indent=2)

    def load_assets(self, filename: str) -> None:
        with open(f"{filename}.json", "r") as f:
            assets = json.load(f)
        self.template = assets["template"]
        self.prompt = assets["prompt"]

# Usage example
if __name__ == "__main__":
    generator = TemplateGenerator(model_name='vendor.py', number_of_samples=1)
    generated_data = generator.test_template()
    # generator.save_assets("vendor_assets")
    # print(f"Template: {generator.template}")
    # print(f"Prompt: {generator.prompt}")
    # print(f"Generated data: {generated_data}")