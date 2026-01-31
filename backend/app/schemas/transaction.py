"""
Transaction schemas
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.product import ProductResponse


class TransactionItemResponse(BaseModel):
    id: int
    product: ProductResponse
    quantity: int
    unit_price: float
    tax_rate: float
    subtotal: float
    
    class Config:
        from_attributes = True


class TransactionResponse(BaseModel):
    id: int
    transaction_id: str
    cart_id: int
    payment_method: str
    amount: float
    status: str
    payment_reference: Optional[str] = None
    items: List[TransactionItemResponse] = []
    receipt_data: Optional[dict] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
