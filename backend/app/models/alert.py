"""
Alert model for theft detection and security events
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class AlertType(str, enum.Enum):
    THEFT_DETECTED = "theft_detected"
    MISMATCH_DETECTED = "mismatch_detected"
    UNSCANNED_ITEM = "unscanned_item"
    REMOVAL_WITHOUT_SCAN = "removal_without_scan"
    EXIT_VALIDATION_FAILED = "exit_validation_failed"
    AI_VERIFICATION_FAILED = "ai_verification_failed"


class AlertSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, enum.Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=True)
    alert_type = Column(Enum(AlertType), nullable=False)
    severity = Column(Enum(AlertSeverity), default=AlertSeverity.MEDIUM)
    status = Column(Enum(AlertStatus), default=AlertStatus.PENDING)
    message = Column(Text, nullable=False)
    details = Column(Text, nullable=True)  # JSON details
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    product = relationship("Product")

    def __repr__(self):
        return f"<Alert(id={self.id}, alert_type={self.alert_type}, severity={self.severity})>"
