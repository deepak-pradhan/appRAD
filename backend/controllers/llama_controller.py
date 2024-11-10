import json
from typing import Any, Dict, List
from fastapi import APIRouter
from backend.controllers.bases.base_llm_controller import BaseLLMController
from backend.models.bases.lmodel import LModel, Function, FunctionCall
from backend.functions.currency_conversion import convert_currency
from backend.functions.language_translation import translate_text
from backend.functions.data_analysis import analyze_data

class LlamaController(BaseLLMController):
    router: APIRouter
    functions: List[Function]  # Add this line to declare the field

    def __init__(self):        
        self.router = APIRouter()
        self.register_additional_routes()
        
        # Initialize with predefined test functions
        self.functions = [
            Function(
                type="function",
                name="get_current_weather",
                description="Get the current weather in a given location",
                parameters={
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string", 
                            "description": "The name of the location/city"
                        },
                    },
                    "required": ["text", "city"]
                }
            ),
            Function(
                type="function",
                name="convert_currency",
                description="Convert an amount from one currency to another",
                parameters={
                    "type": "object",
                    "properties": {
                        "amount": {"type": "number", "description": "Amount to convert"},
                        "from_currency": {"type": "string", "description": "Source currency code"},
                        "to_currency": {"type": "string", "description": "Target currency code"}
                    },
                    "required": ["amount", "from_currency", "to_currency"]
                }
            ),
            Function(
                type="function",
                name="translate_text",
                description="Translate text to a target language",
                parameters={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to translate"},
                        "target_language": {"type": "string", "description": "Target language code"}
                    },
                    "required": ["text", "target_language"]
                }
            ),
            Function(
                name="analyze_data",
                description="Perform data analysis on provided data",
                parameters={
                    "type": "object",
                    "properties": {
                        "data": {"type": "string", "description": "JSON string of data to analyze"},
                        "analysis_type": {"type": "string", "description": "Type of analysis to perform (summary or correlation)"}
                    },
                    "required": ["data", "analysis_type"]
                }
            )
        ]    
        
    def register_additional_routes(self):
        """Register any additional routes specific to this controller"""
        self.router.add_api_route("/chat", self.chat, methods=["POST"], name="chat")
        self.router.add_api_route("/functions", self.list_functions, methods=["GET"], name="list_functions")
        self.router.add_api_route("/models", self.list_models, methods=["GET"], name="list_models")

    async def chat(self, model: LModel):
        try:
            # Get the last user message
            user_message = model.messages[-1].content
            function_call = None
            result = None

            # Check message content and call appropriate function
            if "currency" in user_message.lower():
                function_call = FunctionCall(
                    name="convert_currency", 
                    arguments='{"amount": 100, "from_currency": "USD", "to_currency": "EUR"}'
                )
                result = convert_currency(100, "USD", "EUR")
            elif "translate" in user_message.lower():
                function_call = FunctionCall(
                    name="translate_text", 
                    arguments='{"text": "Hello, world!", "target_language": "es"}'
                )
                result = translate_text("Hello, world!", "es")
            elif "analyze" in user_message.lower():
                sample_data = json.dumps({"col1": [1, 2, 3], "col2": [4, 5, 6]})
                function_call = FunctionCall(
                    name="analyze_data", 
                    arguments=f'{{"data": {sample_data}, "analysis_type": "summary"}}'
                )
                result = analyze_data(sample_data, "summary")

            # If a function was called, include its result in the response
            if result:
                response = f"Based on the {function_call.name} function, here's what I found: {result}"
            else:
                # If no function matches, make a regular LLM request
                conversation_history = self.format_conversation_history(model.messages[:-1])
                full_prompt = f"{conversation_history}\nUser: {user_message}\nAssistant:"
                
                llm_response = await self._make_llm_request("generate", {
                    "model": model.model or "llama2",
                    "prompt": full_prompt,
                    "stream": False
                })
                response = llm_response.get("response", "I'm not sure how to help with that.")

            return self.create_chat_response(response, function_call)

        except Exception as e:
            return self.handle_error(e)

    def get_model_name(self):
        return "llama2"

    def get_usage_info(self):
        return {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }


    def get_available_functions(self) -> List[Any]:
        """Return list of available functions"""
        return [
            {
                "name": "convert_currency",
                "description": "Convert an amount from one currency to another",
                "parameters": {
                    "amount": "float",
                    "from_currency": "str",
                    "to_currency": "str"
                }
            },
            {
                "name": "translate_text",
                "description": "Translate text to target language",
                "parameters": {
                    "text": "str",
                    "target_language": "str"
                }
            },
            {
                "name": "analyze_data",
                "description": "Analyze provided data",
                "parameters": {
                    "data": "json",
                    "analysis_type": "str"
                }
            }
        ]
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """Return available Llama models in OpenAI format"""
        return [
            {
                "id": "llama2",
                "object": "model",
                "created": self.get_current_timestamp(),
                "owned_by": "Meta",
                "permission": [],
                "root": "llama2",
                "parent": None
            }
        ]


llama_controller = LlamaController()
router = llama_controller.router
