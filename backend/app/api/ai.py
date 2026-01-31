"""
AI Verification API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.schemas.ai import AIVerificationRequest, AIVerificationResponse
from app.services.ai_service import ai_service
from app.services.theft_detection_service import theft_detection_service
from app.services.iot_service import iot_service

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/verify", response_model=AIVerificationResponse)
def verify_product(
    request: AIVerificationRequest,
    db: Session = Depends(get_db)
):
    """
    Verify product using AI vision
    """
    cart = db.query(Cart).filter(Cart.id == request.cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    product = db.query(Product).filter(Product.id == request.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Find cart item
    cart_item = next(
        (item for item in cart.items if item.product_id == request.product_id),
        None
    )
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Product not in cart")
    
    # Run AI verification
    verification = ai_service.verify_product(
        product,
        image_data=request.image_data,
        detected_objects=request.detected_objects
    )
    
    # Update cart item
    cart_item.verified_by_ai = verification.verified
    cart_item.scan_verified = True
    db.commit()
    
    # Publish IoT event
    if verification.alert_triggered:
        iot_service.publish_alert_event(
            request.cart_id,
            "ai_verification_failed",
            verification.message,
            "high"
        )
    
    return verification


@router.post("/verify-item/{cart_item_id}", response_model=AIVerificationResponse)
def verify_cart_item(
    cart_item_id: int,
    image_data: str = None,
    db: Session = Depends(get_db)
):
    """
    Verify a specific cart item using AI
    """
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    cart = db.query(Cart).filter(Cart.id == cart_item.cart_id).first()
    
    # Use theft detection service for comprehensive verification
    verified, alert = theft_detection_service.verify_item_with_ai(
        db, cart, cart_item_id, image_data
    )
    
    # Get verification details
    verification = ai_service.verify_product(
        cart_item.product,
        image_data=image_data
    )
    
    return verification
