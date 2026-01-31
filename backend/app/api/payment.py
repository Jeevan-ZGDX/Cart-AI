"""
Payment API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.payment import PaymentRequest, PaymentResponse, QRCodeResponse
from app.services.payment_service import payment_service
from app.services.iot_service import iot_service

router = APIRouter(prefix="/payment", tags=["payment"])


@router.post("/{cart_id}/qr", response_model=QRCodeResponse)
def generate_payment_qr(cart_id: int, db: Session = Depends(get_db)):
    """
    Generate payment QR code for cart
    """
    try:
        qr_response = payment_service.generate_payment_qr(db, cart_id)
        return qr_response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/process", response_model=PaymentResponse)
def process_payment(
    request: PaymentRequest,
    db: Session = Depends(get_db)
):
    """
    Process payment for cart (simulated)
    """
    try:
        payment_response = payment_service.process_payment(
            db,
            request.cart_id,
            request.payment_method,
            payment_reference=None
        )
        
        # Publish IoT event
        iot_service.publish_payment_event(
            request.cart_id,
            payment_response.transaction_id,
            payment_response.amount,
            payment_response.status
        )
        
        return payment_response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
