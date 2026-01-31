"""
Payment schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaymentRequest(BaseModel):
    cart_id: int
    payment_method: str  # "qr_code", "nfc", "card", "cash"


class QRCodeResponse(BaseModel):
    qr_code_data: str  # Base64 encoded QR code image
    payment_reference: str
    amount: float
    expires_at: datetime


class PaymentResponse(BaseModel):
    transaction_id: str
    cart_id: int
    payment_method: str
    amount: float
    status: str
    payment_reference: Optional[str] = None
    receipt_data: Optional[dict] = None
    completed_at: Optional[datetime] = None
