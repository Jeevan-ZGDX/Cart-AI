"""
Product recommendation model
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ProductRecommendation(Base):
    __tablename__ = "product_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    recommended_product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    confidence_score = Column(Float, default=0.0)  # 0.0 to 1.0
    recommendation_type = Column(String(50), nullable=False)  # e.g., "frequently_bought_together", "similar_category"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    product = relationship("Product", foreign_keys=[product_id])
    recommended_product = relationship("Product", foreign_keys=[recommended_product_id])

    def __repr__(self):
        return f"<ProductRecommendation(id={self.id}, product_id={self.product_id}, recommended_product_id={self.recommended_product_id})>"
