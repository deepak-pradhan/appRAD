from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Category(BModel):
    id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    tenant_id: Optional[int] = Field(default=None)
