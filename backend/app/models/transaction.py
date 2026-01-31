"""
Transaction models for payment and receipts
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class PaymentMethod(str, enum.Enum):
    QR_CODE = "qr_code"
    NFC = "nfc"
    CARD = "card"
    CASH = "cash"


class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    transaction_id = Column(String(100), unique=True, nullable=False, index=True)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    payment_qr_code = Column(Text, nullable=True)  # Base64 encoded QR code
    payment_reference = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    receipt_data = Column(Text, nullable=True)  # JSON receipt data
    
    # Relationships
    cart = relationship("Cart", back_populates="transactions")
    items = relationship("TransactionItem", back_populates="transaction", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Transaction(id={self.id}, transaction_id={self.transaction_id}, status={self.status})>"


class TransactionItem(Base):
    __tablename__ = "transaction_items"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    tax_rate = Column(Float, default=0.0)
    subtotal = Column(Float, nullable=False)
    
    # Relationships
    transaction = relationship("Transaction", back_populates="items")
    product = relationship("Product", back_populates="transaction_items")

    def __repr__(self):
        return f"<TransactionItem(id={self.id}, transaction_id={self.transaction_id}, product_id={self.product_id})>"
