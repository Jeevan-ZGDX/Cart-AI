"""
Product schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    sku: str
    barcode: str
    name: str
    description: Optional[str] = None
    price: float
    tax_rate: float = 0.0
    category: str
    aisle_id: Optional[int] = None
    rfid_tag_id: Optional[str] = None
    image_url: Optional[str] = None
    stock_quantity: int = 0


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    is_active: bool
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ProductSearch(BaseModel):
    query: str = Field(..., description="Search query (name, barcode, SKU, or category)")
    limit: int = Field(10, ge=1, le=100)
