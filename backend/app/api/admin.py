"""
Admin Dashboard API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.database import get_db
from app.models.cart import Cart, CartStatus
from app.models.transaction import Transaction
from app.models.product import Product
from app.models.alert import Alert
from app.models.cart import CartItem
from app.schemas.product import ProductResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/analytics/overview")
def get_analytics_overview(db: Session = Depends(get_db)):
    """
    Get overview analytics for admin dashboard
    """
    # Active carts
    active_carts = db.query(Cart).filter(Cart.status == CartStatus.ACTIVE).count()
    
    # Total transactions today
    today = datetime.utcnow().date()
    transactions_today = db.query(Transaction).filter(
        func.date(Transaction.created_at) == today
    ).count()
    
    # Revenue today
    revenue_today = db.query(func.sum(Transaction.amount)).filter(
        func.date(Transaction.created_at) == today,
        Transaction.status == "completed"
    ).scalar() or 0.0
    
    # Active alerts
    active_alerts = db.query(Alert).filter(Alert.is_active == True).count()
    
    # Popular products (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    popular_products = db.query(
        Product.id,
        Product.name,
        func.count(CartItem.id).label('purchase_count')
    ).join(
        CartItem, CartItem.product_id == Product.id
    ).join(
        Cart, Cart.id == CartItem.cart_id
    ).filter(
        Cart.created_at >= week_ago
    ).group_by(
        Product.id, Product.name
    ).order_by(
        desc('purchase_count')
    ).limit(10).all()
    
    return {
        "active_carts": active_carts,
        "transactions_today": transactions_today,
        "revenue_today": round(revenue_today, 2),
        "active_alerts": active_alerts,
        "popular_products": [
            {"product_id": p.id, "name": p.name, "purchase_count": p.purchase_count}
            for p in popular_products
        ]
    }


@router.get("/carts/active")
def get_active_carts(
    limit: int = Query(50, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get all active carts
    """
    carts = db.query(Cart).filter(
        Cart.status == CartStatus.ACTIVE
    ).order_by(Cart.created_at.desc()).limit(limit).all()
    
    return [
        {
            "id": cart.id,
            "session_id": cart.session_id,
            "total_amount": cart.total_amount,
            "final_amount": cart.final_amount,
            "item_count": len(cart.items),
            "has_alert": cart.has_alert,
            "created_at": cart.created_at.isoformat()
        }
        for cart in carts
    ]


@router.get("/products/popular")
def get_popular_products(
    days: int = Query(7, ge=1, le=365),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get popular products by purchase count
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    popular = db.query(
        Product.id,
        Product.name,
        Product.category,
        Product.price,
        func.count(CartItem.id).label('purchase_count'),
        func.sum(CartItem.quantity).label('total_quantity')
    ).join(
        CartItem, CartItem.product_id == Product.id
    ).join(
        Cart, Cart.id == CartItem.cart_id
    ).filter(
        Cart.created_at >= start_date
    ).group_by(
        Product.id, Product.name, Product.category, Product.price
    ).order_by(
        desc('purchase_count')
    ).limit(limit).all()
    
    return [
        {
            "product_id": p.id,
            "name": p.name,
            "category": p.category,
            "price": p.price,
            "purchase_count": p.purchase_count,
            "total_quantity": p.total_quantity
        }
        for p in popular
    ]


@router.get("/alerts/summary")
def get_alerts_summary(
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Get alerts summary by type
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    alerts = db.query(Alert).filter(
        Alert.created_at >= start_date
    ).all()
    
    summary = {}
    for alert in alerts:
        alert_type = alert.alert_type.value
        if alert_type not in summary:
            summary[alert_type] = {
                "count": 0,
                "high_severity": 0,
                "resolved": 0
            }
        
        summary[alert_type]["count"] += 1
        if alert.severity.value == "high" or alert.severity.value == "critical":
            summary[alert_type]["high_severity"] += 1
        if alert.status.value == "resolved":
            summary[alert_type]["resolved"] += 1
    
    return summary


@router.get("/transactions/recent")
def get_recent_transactions(
    limit: int = Query(50, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get recent transactions
    """
    transactions = db.query(Transaction).order_by(
        desc(Transaction.created_at)
    ).limit(limit).all()
    
    return [
        {
            "transaction_id": t.transaction_id,
            "cart_id": t.cart_id,
            "amount": t.amount,
            "payment_method": t.payment_method.value,
            "status": t.status.value,
            "created_at": t.created_at.isoformat(),
            "completed_at": t.completed_at.isoformat() if t.completed_at else None
        }
        for t in transactions
    ]
