"""
Cart and CartItem models
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class CartStatus(str, enum.Enum):
    ACTIVE = "active"
    PAID = "paid"
    ABANDONED = "abandoned"
    ALERT = "alert"


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    status = Column(Enum(CartStatus), default=CartStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    paid_at = Column(DateTime(timezone=True), nullable=True)
    total_amount = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    final_amount = Column(Float, default=0.0)
    has_alert = Column(Boolean, default=False)
    alert_reason = Column(String(500), nullable=True)
    
    # Relationships
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="cart")

    def __repr__(self):
        return f"<Cart(id={self.id}, session_id={self.session_id}, status={self.status})>"


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    tax_rate = Column(Float, default=0.0)
    subtotal = Column(Float, nullable=False)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    verified_by_ai = Column(Boolean, default=False)
    scan_verified = Column(Boolean, default=False)
    
    # Relationships
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items")

    def __repr__(self):
        return f"<CartItem(id={self.id}, cart_id={self.cart_id}, product_id={self.product_id}, quantity={self.quantity})>"
