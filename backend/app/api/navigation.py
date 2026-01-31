"""
Navigation API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.navigation import NavigationRequest, NavigationResponse
from app.services.navigation_service import navigation_service

router = APIRouter(prefix="/navigation", tags=["navigation"])


@router.post("/route", response_model=NavigationResponse)
def get_navigation_route(
    request: NavigationRequest,
    db: Session = Depends(get_db)
):
    """
    Get navigation route to a product or aisle
    """
    try:
        route = navigation_service.get_navigation_route(
            db,
            request.cart_id,
            target_product_id=request.target_product_id,
            target_aisle_id=request.target_aisle_id
        )
        return route
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/map")
def get_store_map():
    """
    Get store map configuration
    """
    return navigation_service.get_store_map()
