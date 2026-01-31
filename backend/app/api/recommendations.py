"""
Recommendations API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.recommendation import RecommendationResponse
from app.services.recommendation_service import recommendation_service

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/cart/{cart_id}", response_model=RecommendationResponse)
def get_recommendations(
    cart_id: int,
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """
    Get product recommendations for a cart
    """
    try:
        recommendations = recommendation_service.get_recommendations(
            db, cart_id, limit
        )
        return recommendations
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
