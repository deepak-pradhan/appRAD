"""
BaseLLMController: Base Controller for Multiple LLM Implementations

Supports:
- Ollama API format
- OpenAI Chat Completion API format
- Llama 3.1 specific features

Core Endpoints:
1. /chat - Handles chat completions
2. /functions - Lists available function calls
3. /models - Lists available models (compatible with OpenAI format)

Standard Response Format:
{
    "id": "chatcmpl-{uuid}",
    "object": "chat.completion", 
    "created": timestamp,
    "model": model_name,
    "choices": [{
        "index": 0,
        "message": {
            "role": "assistant",
            "content": response_text,
            "function_call": optional_function_data
        },
        "finish_reason": "stop"
    }],
    "usage": {
        "prompt_tokens": int,
        "completion_tokens": int,
        "total_tokens": int
    }
}
"""

from abc import ABC, abstractmethod
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel
from backend.models.bases.lmodel import LModel, LModelResponse, ChatMessage, MessageRole, Choice, FinishReason
from typing import List, Dict, Any, ClassVar
import httpx
import logging
import uuid
import time

class BaseLLMController(ABC, SQLModel):
    BASE_URL: ClassVar[str] = "http://localhost:11434/api"    
    router: APIRouter

    class Config:
        arbitrary_types_allowed = True

    def __init__(self):
        self.router = APIRouter()
        self.logger = logging.getLogger(__name__)
        self.register_routes()

    def register_routes(self):
        self.router.add_api_route("/chat", self.chat, methods=["POST"], name="chat")
        self.router.add_api_route("/functions", self.list_functions, methods=["GET"], name="list_functions")
        self.router.add_api_route("/models", self.list_models, methods=["GET"], name="list_models")

    @abstractmethod
    async def chat(self, model: LModel) -> LModelResponse:
        """Process chat messages and return responses."""
        pass

    @abstractmethod
    async def list_models(self) -> List[Dict[str, Any]]:
        """Return available models in OpenAI format"""
        pass

    async def list_functions(self) -> List[Dict[str, Any]]:
        """Return available functions in OpenAI function calling format"""
        return [function.dict() for function in self.get_available_functions()]

    @abstractmethod
    def get_available_functions(self) -> List[Any]:
        """Define available functions. To be implemented by subclasses."""
        pass

    async def _make_llm_request(self, endpoint: str, payload: dict) -> dict:
        """Make a request to the LLM API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.BASE_URL}/{endpoint}",
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            self.logger.error(f"HTTP error occurred: {str(e)}")
            raise HTTPException(status_code=500, detail=f"LLM API error: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error making LLM request: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def create_chat_response(self, content: str, function_call: Any = None) -> LModelResponse:
        """Create a standardized chat response"""
        message = ChatMessage(role=MessageRole.ASSISTANT, content=content)
        if function_call:
            message.function_call = function_call

        choice = Choice(
            index=0,
            message=message,
            finish_reason=FinishReason.STOP if not function_call else FinishReason.FUNCTION_CALL
        )

        return LModelResponse(
            id=f"chatcmpl-{self.generate_unique_id()}",
            object="chat.completion",
            created=self.get_current_timestamp(),
            model=self.get_model_name(),
            choices=[choice.dict()],
            usage=self.get_usage_info()
        )

    def generate_unique_id(self) -> str:
        return str(uuid.uuid4())

    def get_current_timestamp(self) -> int:
        return int(time.time())

    def get_model_name(self) -> str:
        return "base-model"

    def get_usage_info(self) -> Dict[str, int]:
        return {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }

    def format_conversation_history(self, messages: List[ChatMessage]) -> str:
        """Format conversation history into a string"""
        return "\n".join([
            f"{msg.role}: {msg.content}" 
            for msg in messages
        ])

    def handle_error(self, error: Exception) -> LModelResponse:
        """Create an error response"""
        self.logger.error(f"Error processing request: {str(error)}")
        return self.create_chat_response(
            content=f"An error occurred: {str(error)}"
        )