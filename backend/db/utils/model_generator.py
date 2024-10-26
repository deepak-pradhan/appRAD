"""
This class is used to convert a template to model.

1. Read template
import requests
import json
import random

model = "llama3.1:8b"
template = {
  "type": "",
  "name": "",
  "description": "",
  "email": "",
  "phone": "",
  "address": {
    "street": "",
    "city": "",
    "state": "",
    "zipCode": ""
  },
}

prompt = f"Generate 21 synthetic sample data set of a persons with first name, last name, address in the US, and  phone number.\nUse the following template: {json.dumps(template)}."

data = {
    "prompt": prompt,
    "model": model,
    "format": "json",
    "stream": False,
    "options": {"temperature": 2.5, "top_p": 0.99, "top_k": 100},
}

print(f"Generating a sample user")
response = requests.post("http://localhost:11434/api/generate", json=data, stream=False)
json_data = json.loads(response.text)
# print(json.dumps(json.loads(json_data["response"]), indent=2))
json_data
2. Create model file
"""