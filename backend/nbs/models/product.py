from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Product(BModel):
    id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None)
    category_id: Optional[int] = Field(default=None)
    tenant_id: Optional[int] = Field(default=None)
