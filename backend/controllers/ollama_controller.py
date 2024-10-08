import json
import logging
from fastapi import APIRouter
import requests
from backend.models.l_model import LModel

class OllamaController():
    OLLAMA_URL = "http://localhost:11434/api/generate"

    def __init__(self):        
        self.router = APIRouter()
        self.register_additional_routes()
        self.logger = logging.getLogger(__name__)

    def register_additional_routes(self):
        self.router.add_api_route("/chat", self.chat_with_ollama, methods=["POST"], name="chat_with_ollama")
        self.router.add_api_route("/generate_code", self.generate_code, methods=["POST"], name="generate_code")
        self.router.add_api_route("/generate_vendor_description", self.generate_vendor_description, methods=["POST"], name="generate_vendor_description")
    
    async def parse_reponse(response):
        formatted_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    json_line = json.loads(line.decode('utf-8'))        # Parse each line as JSON
                    if "response" in json_line:
                        formatted_response += json_line["response"]     # Extract the response content
                except json.JSONDecodeError:
                    # Handle any decoding errors
                    continue
        
        formatted_response = formatted_response.strip() + "\n"    
        return formatted_response

    @staticmethod
    async def chat_with_ollama(m: LModel):
        headers = {"Content-Type": "application/json"} 
        full_prompt = "\n".join(m.conversation_history + [m.prompt])
        payload = {
                "model": m.model,
                "prompt": full_prompt,
                "temperature": m.temperature,
                "max_tokens": m.max_tokens,
                "stream": False,
        }
        response = requests.post(OllamaController.OLLAMA_URL, json=payload, headers=headers)    
        formatted_response = await OllamaController.parse_reponse(response)
        return {"response": formatted_response}   
    
    @staticmethod
    async def generate_code(m: LModel):
        headers = {"Content-Type": "application/json"}

        full_prompt = f"Generate {m.language} code for the following task:\n{m.prompt}\nOnly return the code, no explanations."

        payload = {
            "model": m.model,
            "prompt": full_prompt,
            "temperature": m.temperature,
            "max_tokens": m.max_tokens,
            "stream": False,
        }

        response = requests.post(OllamaController.OLLAMA_URL, json=payload, headers=headers)    
        formatted_response = await OllamaController.parse_reponse(response)
        return {"code": formatted_response}    
    
    @staticmethod
    async def generate_vendor_description(m: LModel):
        # Implement the logic for generating vendor descriptions here
        # This will be similar to your chat_with_ollama method
        pass

ollama_controller = OllamaController()
router = ollama_controller.router