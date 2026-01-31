"""
Alert schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AlertResponse(BaseModel):
    id: int
    cart_id: Optional[int] = None
    alert_type: str
    severity: str
    status: str
    message: str
    details: Optional[dict] = None
    product_id: Optional[int] = None
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True
