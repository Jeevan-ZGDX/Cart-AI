"""
Alerts API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.alert import Alert, AlertStatus
from app.schemas.alert import AlertResponse
from app.services.theft_detection_service import theft_detection_service

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/", response_model=List[AlertResponse])
def get_alerts(
    cart_id: int = Query(None),
    status: str = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get alerts (optionally filtered by cart_id and status)
    """
    query = db.query(Alert)
    
    if cart_id:
        query = query.filter(Alert.cart_id == cart_id)
    
    if status:
        query = query.filter(Alert.status == AlertStatus(status))
    
    query = query.filter(Alert.is_active == True)
    query = query.order_by(Alert.created_at.desc())
    
    alerts = query.limit(limit).all()
    return alerts


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """
    Get alert by ID
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/{alert_id}/resolve")
def resolve_alert(
    alert_id: int,
    resolution: str = Query("resolved", regex="^(resolved|false_positive|reviewed)$"),
    db: Session = Depends(get_db)
):
    """
    Resolve an alert
    """
    try:
        alert = theft_detection_service.resolve_alert(db, alert_id, resolution)
        return {"message": "Alert resolved", "alert": alert}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
