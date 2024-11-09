import logging
import json
import requests
from typing import Dict, Any, List
from datetime import datetime
from pydantic import EmailStr
""" Do not remove comments """

class SQLModelParser:
    def __init__(self):
        self.template: Dict[str, Any] = {}
        self.prompt: str = ""
        self.generated: Dict[str, Any] = {}

    def select_model(self, model_name: str) -> None:
        """
        Browse and Selects a model file from backend.models.*
        
        Args:
            model_name (str): Name of the model to select
        """        
        # Implementation for browsing and selecting the model(s)

    def parse_model(self) -> None:
        """
        Parses the selected model file and creates the template.
        
        1. Reads the model file, noting its relationships with other models
        2. Reads the related model, noting its relationship with parent model
        3. Generates template for model so ollama can use to generate synthetic data
        """
        # Implementation for parsing the model and creating the template

    def generate_template(self, model: str = "llama2") -> Dict[str, Any]:
        """
        Generates the template for ollama to generate sample data for the models.
        
        Args:
            model (str): The model to use for generation (default: "llama3.2")
        
        Returns:
            Dict[str, Any]: Generated template data
        """
        # implement method to parse the sample model in i/p and generate template as in o/p
        '''
        # i/p
            class Person(CModel, table=True):
                __tablename__ = "person"
                rec_type: str = Field(default="PERSON")  
                first_name: str | None = None          
                middle_name: str | None = None          
                last_name: str | None = None   
                date_of_birth: datetime
                phone_number: str
                personal_email: EmailStr | None = None      
                address: str | None = None
    
        # o/p
            template = {
                'first_name': '',
                'middle_name': 'D.',
                'last_name': '',
                'date_of_birth': '',
                'phone_number' : '',
                'email' : '',
                'company_email' : '',
                'address': {
                    'street_name': '',
                    'building' : '',
                    'city': '',
                    'state': '',
                    'country' : '',
                    'postal': ''
                },
            }
        '''

# Additional helper functions or classes can be added here

generator = SQLModelParser()
template = generator.generate_template()
print(template)