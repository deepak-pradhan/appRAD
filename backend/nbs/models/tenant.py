from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Tenant(BModel):
    tenant_id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
