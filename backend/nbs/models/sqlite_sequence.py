from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class sqlite_sequence(BModel):
    name: Optional[str] = Field(default=None)
    seq: Optional[str] = Field(default=None)
