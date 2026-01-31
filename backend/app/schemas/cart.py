"""
Cart schemas
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.product import ProductResponse


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product: ProductResponse
    quantity: int
    unit_price: float
    tax_rate: float
    subtotal: float
    verified_by_ai: bool
    scan_verified: bool
    added_at: datetime
    
    class Config:
        from_attributes = True


class CartCreate(BaseModel):
    session_id: str


class CartUpdate(BaseModel):
    status: Optional[str] = None


class CartResponse(BaseModel):
    id: int
    session_id: str
    status: str
    total_amount: float
    tax_amount: float
    discount_amount: float
    final_amount: float
    has_alert: bool
    alert_reason: Optional[str] = None
    items: List[CartItemResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
