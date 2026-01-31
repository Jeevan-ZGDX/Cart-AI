"""
Recommendation schemas
"""
from pydantic import BaseModel
from typing import List
from app.schemas.product import ProductResponse


class RecommendationItem(BaseModel):
    product: ProductResponse
    confidence_score: float
    recommendation_type: str
    reason: str


class RecommendationResponse(BaseModel):
    cart_id: int
    recommendations: List[RecommendationItem]
    based_on_items: List[int]  # Product IDs in cart
