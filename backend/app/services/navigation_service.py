"""
Navigation Service
Handles store map navigation and aisle routing
"""
import json
import math
from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from app.models.aisle import Aisle
from app.models.product import Product
from app.models.cart import Cart
from app.schemas.navigation import NavigationResponse, NavigationStep, AisleResponse


class NavigationService:
    """Service for store navigation and routing"""
    
    def __init__(self):
        # Store map configuration
        # In production, this would be loaded from database or config file
        self.store_map = {
            "width": 100,  # Store width in units
            "height": 100,  # Store height in units
            "entrance": (0, 0),  # Entrance coordinates
            "checkout": (90, 90)  # Checkout coordinates
        }
    
    def calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """
        Calculate Euclidean distance between two points
        """
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def find_shortest_path(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        aisles: List[Aisle]
    ) -> List[NavigationStep]:
        """
        Find shortest path through aisles (simplified A* or Dijkstra)
        For demo, using simple direct path with waypoints
        """
        steps = []
        
        # Simple path: direct line with intermediate waypoints at aisles
        # In production, use proper pathfinding algorithm
        
        # Find nearest aisle to start
        nearest_start_aisle = min(
            aisles,
            key=lambda a: self.calculate_distance(start, (a.x_coordinate, a.y_coordinate))
        )
        
        # Find nearest aisle to end
        nearest_end_aisle = min(
            aisles,
            key=lambda a: self.calculate_distance(end, (a.x_coordinate, a.y_coordinate))
        )
        
        step_num = 1
        
        # Step 1: Go to nearest aisle from start
        if nearest_start_aisle.id != nearest_end_aisle.id:
            steps.append(NavigationStep(
                step_number=step_num,
                instruction=f"Navigate to {nearest_start_aisle.section} section",
                aisle_id=nearest_start_aisle.id,
                aisle_name=nearest_start_aisle.name,
                coordinates=(nearest_start_aisle.x_coordinate, nearest_start_aisle.y_coordinate)
            ))
            step_num += 1
        
        # Step 2: Navigate through intermediate aisles if needed
        # (Simplified - in production, calculate optimal path)
        
        # Step 3: Go to target aisle
        steps.append(NavigationStep(
            step_number=step_num,
            instruction=f"Arrive at {nearest_end_aisle.name} in {nearest_end_aisle.section} section",
            aisle_id=nearest_end_aisle.id,
            aisle_name=nearest_end_aisle.name,
            coordinates=(nearest_end_aisle.x_coordinate, nearest_end_aisle.y_coordinate)
        ))
        
        return steps
    
    def get_navigation_route(
        self,
        db: Session,
        cart_id: int,
        target_product_id: Optional[int] = None,
        target_aisle_id: Optional[int] = None
    ) -> NavigationResponse:
        """
        Get navigation route to a product or aisle
        """
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        if not cart:
            raise ValueError(f"Cart {cart_id} not found")
        
        # Determine target
        if target_product_id:
            product = db.query(Product).filter(Product.id == target_product_id).first()
            if not product:
                raise ValueError(f"Product {target_product_id} not found")
            
            if not product.aisle_id:
                raise ValueError(f"Product {target_product_id} has no aisle assigned")
            
            target_aisle = db.query(Aisle).filter(Aisle.id == product.aisle_id).first()
        elif target_aisle_id:
            target_aisle = db.query(Aisle).filter(Aisle.id == target_aisle_id).first()
            if not target_aisle:
                raise ValueError(f"Aisle {target_aisle_id} not found")
        else:
            raise ValueError("Either target_product_id or target_aisle_id must be provided")
        
        # Get all aisles for pathfinding
        all_aisles = db.query(Aisle).all()
        
        # Current location (simulated - in production, get from cart GPS/RFID)
        current_location = self.store_map["entrance"]
        
        # Calculate route
        target_coords = (target_aisle.x_coordinate, target_aisle.y_coordinate)
        route_steps = self.find_shortest_path(current_location, target_coords, all_aisles)
        
        # Calculate total distance
        total_distance = 0.0
        prev_point = current_location
        for step in route_steps:
            total_distance += self.calculate_distance(prev_point, step.coordinates)
            prev_point = step.coordinates
        
        # Estimate time (assuming 1 unit = 1 meter, walking speed = 1 m/s)
        estimated_time = total_distance / 1.0  # seconds
        estimated_time_minutes = estimated_time / 60.0
        
        return NavigationResponse(
            cart_id=cart_id,
            current_location=current_location,
            target_location=target_coords,
            target_aisle=AisleResponse(
                id=target_aisle.id,
                name=target_aisle.name,
                section=target_aisle.section,
                x_coordinate=target_aisle.x_coordinate,
                y_coordinate=target_aisle.y_coordinate,
                description=target_aisle.description
            ),
            route=route_steps,
            total_distance=round(total_distance, 2),
            estimated_time_minutes=round(estimated_time_minutes, 2)
        )
    
    def get_store_map(self) -> dict:
        """
        Get store map configuration
        """
        return self.store_map


# Global navigation service instance
navigation_service = NavigationService()
