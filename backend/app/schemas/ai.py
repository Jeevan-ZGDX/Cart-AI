"""
AI verification schemas
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class AIVerificationRequest(BaseModel):
    cart_id: int
    product_id: int
    image_data: Optional[str] = None  # Base64 encoded image
    detected_objects: Optional[List[Dict[str, Any]]] = None  # If pre-processed


class AIVerificationResponse(BaseModel):
    verified: bool
    confidence: float
    detected_product_id: Optional[int] = None
    detected_product_name: Optional[str] = None
    match_score: float
    alert_triggered: bool
    message: str
    details: Optional[Dict[str, Any]] = None
