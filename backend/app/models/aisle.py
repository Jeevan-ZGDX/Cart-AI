"""
Aisle model for store navigation
"""
from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Aisle(Base):
    __tablename__ = "aisles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    section = Column(String(50), nullable=False)  # e.g., "A", "B", "C"
    x_coordinate = Column(Float, nullable=False)  # Store map coordinates
    y_coordinate = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    
    # Relationships
    products = relationship("Product", back_populates="aisle")

    def __repr__(self):
        return f"<Aisle(id={self.id}, name={self.name}, section={self.section})>"
