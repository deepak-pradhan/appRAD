"""
The `PersonGenerator` class is responsible for generating synthetic sample data for a person
, including first name, last name, address, and phone number. It uses a pre-defined template to generate the data and provides a method to validate the generated data.

The `_generator` method is the main implementation for generating the person data. It sends a request to a local API endpoint to generate the data based on the provided prompt and template. The method handles any exceptions that may occur during the request and parsing of the response.

The `generate` method is a wrapper around the `_generator` method that ensures the generated data is valid and returns it.

The `validate_person_data` static method checks that the provided person data dictionary contains all the required fields, including first name, last name, address, and phone number.
"""
import requests
import json
# from backend.models.person import Person
import logging
from typing import Dict, Optional
import yaml

import os

model = os.environ.get('LLAMA_MODEL', 'llama3.2')
api_url = os.environ.get('LLAMA_API_URL', 'http://localhost:11434/api/generate')

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def requests_retry_session(retries=3, backoff_factor=0.3):
    session = requests.Session()
    retry = Retry(total=retries, backoff_factor=backoff_factor)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

class PersonGenerator:
    def __init__(self) -> None:
        self.generated = set()      
        #@TODO: read Person model
        # , auto create self.tempalte
        # , find means for RI
        self.template = {
            'first_name': '',
            'middle_name': 'D.',
            'last_name': '',
            'suffix': '',
            'prefix': '',
            'date_of_birth': '',
            'ssn' : '',
            'job' : '',
            'company' : '',
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
        self.prompt = f""" Generate a synthetic sample data set of a persons with first name, last name, address in the US, and  phone number. Use the following template: {json.dumps(self.template)}. """

        
    def _generator(self) -> Optional[Dict]:
        
        data = {
          'prompt': self.prompt,
          'model': model,
          'format': 'json',
          'stream': False,
          'options': {'temperature': 1, 'top_p': 0.99, 'top_k': 100}
        }        

        logging.info("Generating a sample Person")
        try:
            response = requests.post('http://localhost:11434/api/generate', json=data, stream=False)
            response.raise_for_status()
            json_data = json.loads(response.text)
            logging.debug(f"Response: {response.text}")
            logging.debug(f"Parsed JSON: {json_data}")
            if isinstance(json_data, dict) and all(key in json_data for key in self.template.keys()):
                self.generated = json_data
                return json_data
            else:
                logging.error("Received unexpected data format")
                return None
        except requests.RequestException as e:
            logging.error(f"HTTP request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            logging.error(f"JSON parsing failed: {e}")
            return None        
        
    def generate(self) -> Optional[Dict]:
        dd = self._generator()
        if dd:
            return dd        

    @staticmethod     
    def validate_person_data(data: Dict) -> bool:
      """
      A list of required fields that must be present in a person data dictionary.
      
      The `validate_person_data` function checks that the provided `data` dictionary contains all of these required fields.
      """
      required_fields = ['first_name', 'last_name', 'address', 'phone_number']
      return all(field in data for field in required_fields) and isinstance(data['address'], dict)

    
class PersonGenerator:
    def __init__(self):
        with open('person_config.yaml', 'r') as config_file:
            config = yaml.safe_load(config_file)
            self.template = config['template']
            self.prompt = config['prompt']

c = PersonGenerator()
ddd = c.generate()
print(ddd)
