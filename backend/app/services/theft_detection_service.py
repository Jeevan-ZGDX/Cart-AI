"""
Theft Detection Service
Monitors cart for suspicious activities and triggers alerts
"""
from sqlalchemy.orm import Session
from app.models.cart import Cart, CartItem
from app.models.alert import Alert, AlertType, AlertSeverity, AlertStatus
from app.models.product import Product
from app.services.ai_service import ai_service
from typing import List, Optional


class TheftDetectionService:
    """Service for detecting theft and suspicious activities"""
    
    def check_cart_for_theft(
        self,
        db: Session,
        cart: Cart,
        detected_objects: Optional[List[dict]] = None
    ) -> List[Alert]:
        """
        Comprehensive theft detection check
        Returns list of alerts if any suspicious activity detected
        """
        alerts = []
        
        # 1. Check for unscanned items (camera detected but no scan)
        unscanned_alerts = self._check_unscanned_items(db, cart, detected_objects)
        alerts.extend(unscanned_alerts)
        
        # 2. Check for scan-remove mismatch
        mismatch_alerts = self._check_scan_remove_mismatch(db, cart)
        alerts.extend(mismatch_alerts)
        
        # 3. Check for AI verification failures
        ai_alerts = self._check_ai_verification_failures(db, cart)
        alerts.extend(ai_alerts)
        
        # Update cart alert status
        if alerts:
            cart.has_alert = True
            cart.alert_reason = "; ".join([alert.message for alert in alerts[:3]])
            db.commit()
        
        return alerts
    
    def _check_unscanned_items(
        self,
        db: Session,
        cart: Cart,
        detected_objects: Optional[List[dict]]
    ) -> List[Alert]:
        """
        Check if camera detected items that weren't scanned
        """
        alerts = []
        
        if not detected_objects:
            return alerts
        
        # Get scanned product IDs
        scanned_product_ids = {item.product_id for item in cart.items if item.scan_verified}
        
        # Check if detected objects match scanned items
        # This is simplified - in production, use proper object matching
        detected_count = len(detected_objects)
        scanned_count = len(scanned_product_ids)
        
        if detected_count > scanned_count:
            # More items detected than scanned
            alert = Alert(
                cart_id=cart.id,
                alert_type=AlertType.UNSCANNED_ITEM,
                severity=AlertSeverity.HIGH,
                status=AlertStatus.PENDING,
                message=f"Detected {detected_count} items but only {scanned_count} scanned",
                details={"detected_count": detected_count, "scanned_count": scanned_count}
            )
            db.add(alert)
            alerts.append(alert)
        
        return alerts
    
    def _check_scan_remove_mismatch(
        self,
        db: Session,
        cart: Cart
    ) -> List[Alert]:
        """
        Check if items were removed without proper scan removal
        """
        alerts = []
        
        # Check for items marked as removed but still in cart
        # This would require a removal log - simplified for demo
        
        # Check for items with scan_verified=False but in cart
        unverified_items = [item for item in cart.items if not item.scan_verified]
        
        if unverified_items:
            alert = Alert(
                cart_id=cart.id,
                alert_type=AlertType.MISMATCH_DETECTED,
                severity=AlertSeverity.MEDIUM,
                status=AlertStatus.PENDING,
                message=f"{len(unverified_items)} items in cart without scan verification",
                details={"unverified_count": len(unverified_items)}
            )
            db.add(alert)
            alerts.append(alert)
        
        return alerts
    
    def _check_ai_verification_failures(
        self,
        db: Session,
        cart: Cart
    ) -> List[Alert]:
        """
        Check for AI verification failures
        """
        alerts = []
        
        # Check items that failed AI verification
        failed_items = [
            item for item in cart.items
            if item.verified_by_ai == False and item.scan_verified == True
        ]
        
        if failed_items:
            for item in failed_items:
                alert = Alert(
                    cart_id=cart.id,
                    product_id=item.product_id,
                    alert_type=AlertType.AI_VERIFICATION_FAILED,
                    severity=AlertSeverity.MEDIUM,
                    status=AlertStatus.PENDING,
                    message=f"AI verification failed for {item.product.name}",
                    details={"cart_item_id": item.id, "product_id": item.product_id}
                )
                db.add(alert)
                alerts.append(alert)
        
        return alerts
    
    def verify_item_with_ai(
        self,
        db: Session,
        cart: Cart,
        cart_item_id: int,
        image_data: Optional[str] = None
    ) -> tuple[bool, Optional[Alert]]:
        """
        Verify a cart item using AI and create alert if mismatch
        """
        cart_item = next((item for item in cart.items if item.id == cart_item_id), None)
        if not cart_item:
            return False, None
        
        # Run AI verification
        verification = ai_service.verify_product(
            cart_item.product,
            image_data=image_data
        )
        
        # Update cart item
        cart_item.verified_by_ai = verification.verified
        db.commit()
        
        # Create alert if verification failed
        alert = None
        if not verification.verified:
            alert = Alert(
                cart_id=cart.id,
                product_id=cart_item.product_id,
                alert_type=AlertType.AI_VERIFICATION_FAILED,
                severity=AlertSeverity.HIGH,
                status=AlertStatus.PENDING,
                message=verification.message,
                details={
                    "confidence": verification.confidence,
                    "match_score": verification.match_score
                }
            )
            db.add(alert)
            db.commit()
        
        return verification.verified, alert
    
    def resolve_alert(
        self,
        db: Session,
        alert_id: int,
        resolution: str = "resolved"
    ) -> Alert:
        """
        Resolve an alert
        """
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            raise ValueError(f"Alert {alert_id} not found")
        
        if resolution == "resolved":
            alert.status = AlertStatus.RESOLVED
        elif resolution == "false_positive":
            alert.status = AlertStatus.FALSE_POSITIVE
        else:
            alert.status = AlertStatus.REVIEWED
        
        from datetime import datetime
        alert.resolved_at = datetime.utcnow()
        alert.is_active = False
        
        db.commit()
        db.refresh(alert)
        
        return alert


# Global theft detection service instance
theft_detection_service = TheftDetectionService()
