"""
Product model
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    barcode = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    tax_rate = Column(Float, default=0.0)  # Tax percentage
    category = Column(String(100), index=True)
    aisle_id = Column(Integer, ForeignKey("aisles.id"), nullable=True)
    rfid_tag_id = Column(String(100), unique=True, nullable=True)
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    stock_quantity = Column(Integer, default=0)
    
    # Relationships
    aisle = relationship("Aisle", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")
    transaction_items = relationship("TransactionItem", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, sku={self.sku})>"
