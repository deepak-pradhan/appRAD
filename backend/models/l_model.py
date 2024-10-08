from typing import Optional, List, TypeVar

from sqlmodel import Field, SQLModel

T = TypeVar('T', bound='LModel')

class LModel(SQLModel, table=False):
    model       : str = "llama3.1:8b"
    prompt      : str = ''
    temperature : float = 0.7
    max_tokens  : int = 100
    stop        : Optional[List[str]] = None
    user_id     : str | None = None
    request_id  : str | None = None
    stream      : bool = False
    conversation_history: List[str] = []
    language: str = "python"  # Add this line with a default value



class LModelResponse(SQLModel, table=False):
    model               : str           = Field(..., description="Model used for the chat.")
    created_at          : int           = Field(..., description="Timestamp of the chat completion.")
    response            : str           = Field(..., description="Response of the chat completion.")
    done                : bool          = Field(..., description="Whether the chat completion is done.")
    done_reason         : str | None    = Field(None, description="Reason why the chat completion is done.")
    context             : str | None    = Field(None, description="The context of the chat completion.")
    total_duration      : int           = Field(..., description="The total duration of the chat completion.")
    load_duration       : int           = Field(..., description="The load duration of the chat completion.")
    prompt_eval_count   : int           = Field(..., description="The prompt eval count of the chat completion.")
    prompt_eval_duration: int           = Field(..., description="The prompt eval duration of the chat completion.")
    eval_count          : int           = Field(..., description="The eval count of the chat completion.")
    eval_duration       : int           = Field(..., description="The eval duration of the chat completion.")
    tokens_used         : int           = Field(..., description="The number of tokens used in the chat completion.")
