from sqlmodel import Field, Relationship
from decimal import Decimal
from sbox1.backend.models.bases.bmodel import BModel
# from backend.models.vendor import Vendor

class Product(BModel, table=True):
    __tablename__ = "product"
    type: str = "product"
    name: str = Field(index=True)
    description: str = Field(default=None)
    vendor_id: int = Field(foreign_key="vendor.id")
    price: Decimal = Field(max_digits=10, decimal_places=2)
    sku: str = Field(unique=True)
    stock_quantity: int = Field(default=0)
    vendor: "Vendor" = Relationship(back_populates="products")

    def validate(self) -> None:
        super().validate()
        if self.price <= 0:
            raise ValueError("Price must be greater than zero")
        if not self.sku:
            raise ValueError("SKU is required")

from sbox1.backend.models.vendor import Vendor  # At the bottom of product.py
