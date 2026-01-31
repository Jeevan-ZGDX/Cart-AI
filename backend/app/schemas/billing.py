"""
Billing schemas
"""
from pydantic import BaseModel
from typing import List, Optional
from app.schemas.cart import CartItemResponse


class BillCalculation(BaseModel):
    subtotal: float
    tax_amount: float
    discount_amount: float
    final_amount: float
    item_count: int


class BillingResponse(BaseModel):
    cart_id: int
    session_id: str
    calculation: BillCalculation
    items: List[CartItemResponse]
    currency: str = "USD"
