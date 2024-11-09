"""
Includes classes for structured message handling
, function calling capabilities
, and response structure for an LModel.

The `FunctionCall` class represents a function call with a name and arguments.

The `Function` class represents a function with a name, description, and parameters.

The `ChatMessage` class represents a chat message with a role
, content, optional name, and optional function call.

The `LModel` class is a SQLModel that includes the `Function` and `FunctionCall` classes
, and various parameters for configuring the language model.

The `LModelResponse` class mirrors the response structure of OpenAI's chat completion API.
"""
from enum import Enum
from typing import List, Dict, Optional, TypeVar, Union
from sqlmodel import SQLModel, Field
from pydantic import BaseModel, field_validator
from abc import ABC

T = TypeVar('T', bound='LModel')


class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"

class FinishReason(Enum):
    STOP = "stop"
    LENGTH = "length"
    FUNCTION_CALL = "function_call"
    # Add other possible finish reasons
    
class FunctionCall(BaseModel):
    name: str
    arguments: str

class Function(BaseModel):
    name: str
    description: str
    parameters: Dict[str, object]


class ChatMessage(BaseModel):
    '''Uses ChatMessage for structured message handling.'''
    role: MessageRole
    content: str
    name: Optional[str] = None
    function_call: Optional[FunctionCall] = None

class Choice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: FinishReason

class LModel(ABC, SQLModel, table=False):
    '''Includes Function and FunctionCall classes for function calling capabilities.'''
    def __init__(self, messages: List[ChatMessage] = None, **kwargs):
        super().__init__(**kwargs)
        self.messages = messages or None
        self._function_names = set()
        
    model: str = "llama3.1:8b"
    messages: List[ChatMessage] = Field(default=[])
    functions: List[Function] = Field(default_factory=list)
    function_call: Optional[Union[str, FunctionCall]] = None
    temperature: float = 0.7
    top_p: float = 1.0
    n: int = 1
    stream: bool = False
    stop: Optional[Union[str, List[str]]] = None
    max_tokens: Optional[int] = None
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    logit_bias: Optional[Dict[int, float]] = None
    user: Optional[str] = None

    def add_message(self, role: MessageRole, content: str, name: Optional[str] = None) -> None: 
        self.messages.append(ChatMessage(role=role, content=content, name=name))


    def add_function(self, function: Function) -> None:
        """
        Adds a new function to the LModel's functions list.        
        Args:
            function (Function): The function to be added.        
        Raises:
            ValueError: If a function with the same name already exists
        """
        if self.functions is None:
            self.functions = []

        if any(function.name in self.functions):
            raise ValueError(f"Function with name '{function.name}' already exists")

        self._function_names.add(function.name)
        self.functions.append(function)
        return True


    def remove_function(self, function_name: str) -> None:
        """
        Removes a function from the LModel's functions list.    
        Args:
            function_name (str): The name of the function to be removed.
        Raises:
            ValueError: If the function with the given name doesn't exist.
        """
        for function in self.functions:
            if function.name == function_name:
                self.functions.remove(function)
                return
    
        raise ValueError(f"Function with name '{function_name}' does not exist")


    @field_validator('temperature', 'top_p')
    def check_probability(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Must be between 0 and 1')
        return v
    
    @field_validator('max_tokens')
    def check_max_tokens(cls, v):
        if v is not None and v <= 0:
            raise ValueError('max_tokens must be a positive integer')
        return v

    def clear_messages(self) -> None:
        """ Clears all messages from the LModel's message list. """
        self.messages.clear()

class LModelResponse(SQLModel, table=False):
    '''Adds an LModelResponse class that mirrors OpenAI's response structure.'''
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Dict[str, Union[str, int, ChatMessage]]]
    usage: Dict[str, int]