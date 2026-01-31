"""
Cart API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cart import Cart, CartItem, CartStatus
from app.schemas.cart import CartCreate, CartResponse, CartItemCreate, CartItemResponse, CartUpdate
from app.schemas.billing import BillingResponse
from app.services.billing_service import BillingService
from app.services.iot_service import iot_service
import uuid

router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("/", response_model=CartResponse)
def create_cart(cart_data: CartCreate, db: Session = Depends(get_db)):
    """
    Create a new cart session
    """
    # Generate session ID if not provided
    session_id = cart_data.session_id or f"CART-{uuid.uuid4().hex[:8].upper()}"
    
    # Check if session already exists
    existing_cart = db.query(Cart).filter(Cart.session_id == session_id).first()
    if existing_cart and existing_cart.status == CartStatus.ACTIVE:
        return existing_cart
    
    cart = Cart(session_id=session_id, status=CartStatus.ACTIVE)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    
    return cart


@router.get("/{cart_id}", response_model=CartResponse)
def get_cart(cart_id: int, db: Session = Depends(get_db)):
    """
    Get cart by ID
    """
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.get("/session/{session_id}", response_model=CartResponse)
def get_cart_by_session(session_id: str, db: Session = Depends(get_db)):
    """
    Get cart by session ID
    """
    cart = db.query(Cart).filter(Cart.session_id == session_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.post("/{cart_id}/items", response_model=CartItemResponse)
def add_item_to_cart(
    cart_id: int,
    item: CartItemCreate,
    db: Session = Depends(get_db)
):
    """
    Add item to cart
    """
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    if cart.status != CartStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Cart is not active")
    
    cart_item = BillingService.add_item_to_cart(
        db, cart, item.product_id, item.quantity
    )
    
    # Publish IoT event
    iot_service.publish_scan_event(cart_id, item.product_id, "")
    iot_service.publish_cart_update(cart_id, cart.final_amount, len(cart.items))
    
    return cart_item


@router.delete("/{cart_id}/items/{item_id}")
def remove_item_from_cart(
    cart_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Remove item from cart
    """
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    success = BillingService.remove_item_from_cart(db, cart, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # Publish IoT event
    iot_service.publish_cart_update(cart_id, cart.final_amount, len(cart.items))
    
    return {"message": "Item removed from cart"}


@router.get("/{cart_id}/billing", response_model=BillingResponse)
def get_cart_billing(cart_id: int, db: Session = Depends(get_db)):
    """
    Get cart billing details
    """
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    return BillingService.get_billing_response(cart)


@router.put("/{cart_id}", response_model=CartResponse)
def update_cart(
    cart_id: int,
    cart_update: CartUpdate,
    db: Session = Depends(get_db)
):
    """
    Update cart status
    """
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    if cart_update.status:
        cart.status = CartStatus(cart_update.status)
    
    db.commit()
    db.refresh(cart)
    
    return cart
