"""
AI Vision Verification Service
Handles product detection and verification using YOLOv8 or fallback methods
"""
import os
import base64
import io
from typing import Optional, Dict, Any, List
from PIL import Image
import numpy as np
from app.config import settings
from app.models.product import Product
from app.schemas.ai import AIVerificationResponse


class AIService:
    """Service for AI-based product verification"""
    
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self._load_model()
    
    def _load_model(self):
        """
        Load YOLOv8 model or set up mock mode
        """
        try:
            if settings.AI_MODEL_PATH and os.path.exists(settings.AI_MODEL_PATH):
                from ultralytics import YOLO
                self.model = YOLO(settings.AI_MODEL_PATH)
                self.model_loaded = True
                print(f"✅ AI Model loaded from {settings.AI_MODEL_PATH}")
            else:
                print("⚠️  AI Model path not provided or not found. Using mock mode.")
                self.model_loaded = False
        except Exception as e:
            print(f"⚠️  Failed to load AI model: {e}. Using mock mode.")
            self.model_loaded = False
    
    def _decode_image(self, image_data: str) -> Optional[Image.Image]:
        """
        Decode base64 image data
        """
        try:
            if image_data.startswith('data:image'):
                # Remove data URL prefix
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            return image.convert('RGB')
        except Exception as e:
            print(f"Error decoding image: {e}")
            return None
    
    def _mock_detection(self, product: Product) -> Dict[str, Any]:
        """
        Mock detection for demo purposes when model is not available
        Returns a simulated detection result
        """
        import random
        
        # Simulate detection with some randomness
        confidence = random.uniform(0.7, 0.95)
        match = random.choice([True, True, True, False])  # 75% match rate
        
        return {
            "detected_product_id": product.id if match else None,
            "detected_product_name": product.name if match else "Unknown Product",
            "confidence": confidence,
            "match": match,
            "bbox": [100, 100, 200, 200],  # Mock bounding box
            "class_id": product.category
        }
    
    def detect_products(self, image: Image.Image) -> List[Dict[str, Any]]:
        """
        Detect products in image using YOLOv8 or mock
        """
        if not self.model_loaded:
            # Return mock detection
            return []
        
        try:
            # Run YOLOv8 inference
            results = self.model(image, conf=settings.AI_CONFIDENCE_THRESHOLD)
            
            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    detection = {
                        "confidence": float(box.conf[0]),
                        "bbox": box.xyxy[0].tolist(),
                        "class_id": int(box.cls[0]),
                        "class_name": result.names[int(box.cls[0])]
                    }
                    detections.append(detection)
            
            return detections
        except Exception as e:
            print(f"Error in product detection: {e}")
            return []
    
    def verify_product(
        self,
        product: Product,
        image_data: Optional[str] = None,
        detected_objects: Optional[List[Dict[str, Any]]] = None
    ) -> AIVerificationResponse:
        """
        Verify if detected product matches scanned product
        """
        # If no model loaded, use mock verification
        if not self.model_loaded:
            mock_result = self._mock_detection(product)
            match_score = mock_result["confidence"] if mock_result["match"] else 0.3
            
            return AIVerificationResponse(
                verified=mock_result["match"],
                confidence=mock_result["confidence"],
                detected_product_id=mock_result["detected_product_id"],
                detected_product_name=mock_result["detected_product_name"],
                match_score=match_score,
                alert_triggered=not mock_result["match"],
                message="Mock verification: " + ("Match confirmed" if mock_result["match"] else "Mismatch detected"),
                details=mock_result
            )
        
        # Real AI verification
        if image_data:
            image = self._decode_image(image_data)
            if not image:
                return AIVerificationResponse(
                    verified=False,
                    confidence=0.0,
                    match_score=0.0,
                    alert_triggered=True,
                    message="Failed to decode image"
                )
            
            detections = self.detect_products(image)
        elif detected_objects:
            detections = detected_objects
        else:
            return AIVerificationResponse(
                verified=False,
                confidence=0.0,
                match_score=0.0,
                alert_triggered=True,
                message="No image data or detections provided"
            )
        
        # Match detection with product
        # This is simplified - in production, you'd match class names or use embeddings
        best_match = None
        best_confidence = 0.0
        
        for detection in detections:
            # Simple matching logic - in production, use product embeddings
            class_name = detection.get("class_name", "").lower()
            product_name = product.name.lower()
            product_category = product.category.lower()
            
            # Check if detection matches product category or name
            if (class_name in product_category or 
                class_name in product_name or
                product_category in class_name):
                if detection["confidence"] > best_confidence:
                    best_confidence = detection["confidence"]
                    best_match = detection
        
        if best_match and best_confidence >= settings.AI_CONFIDENCE_THRESHOLD:
            match_score = best_confidence
            verified = True
            alert_triggered = False
            message = f"Product verified with {best_confidence:.2%} confidence"
        else:
            match_score = best_confidence if best_match else 0.0
            verified = False
            alert_triggered = True
            message = "Product mismatch detected - alert triggered"
        
        return AIVerificationResponse(
            verified=verified,
            confidence=best_confidence,
            detected_product_id=product.id if verified else None,
            detected_product_name=product.name if verified else "Unknown",
            match_score=match_score,
            alert_triggered=alert_triggered,
            message=message,
            details={
                "detections": detections,
                "best_match": best_match
            }
        )


# Global AI service instance
ai_service = AIService()
