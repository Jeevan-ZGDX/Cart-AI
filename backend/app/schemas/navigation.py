"""
Navigation schemas
"""
from pydantic import BaseModel
from typing import List, Optional, Tuple


class AisleResponse(BaseModel):
    id: int
    name: str
    section: str
    x_coordinate: float
    y_coordinate: float
    description: Optional[str] = None
    
    class Config:
        from_attributes = True


class NavigationRequest(BaseModel):
    cart_id: int
    target_product_id: Optional[int] = None
    target_aisle_id: Optional[int] = None


class NavigationStep(BaseModel):
    step_number: int
    instruction: str
    aisle_id: int
    aisle_name: str
    coordinates: Tuple[float, float]


class NavigationResponse(BaseModel):
    cart_id: int
    current_location: Optional[Tuple[float, float]] = None
    target_location: Tuple[float, float]
    target_aisle: AisleResponse
    route: List[NavigationStep]
    total_distance: float
    estimated_time_minutes: float
