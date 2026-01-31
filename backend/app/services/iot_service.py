"""
IoT Messaging Simulation Service
Simulates MQTT-style event messaging for cart events
"""
import json
import asyncio
from typing import Dict, Any, Callable, Optional
from datetime import datetime
from app.config import settings


class IoTService:
    """
    IoT Messaging Service - Simulates MQTT pub/sub for cart events
    In production, this would connect to a real MQTT broker
    """
    
    def __init__(self):
        self.subscribers: Dict[str, list] = {}  # topic -> list of callbacks
        self.message_history: list = []  # Store recent messages for debugging
    
    def publish(self, topic: str, payload: Dict[str, Any]) -> bool:
        """
        Publish message to topic (simulated MQTT publish)
        """
        message = {
            "topic": topic,
            "payload": payload,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.message_history.append(message)
        # Keep only last 1000 messages
        if len(self.message_history) > 1000:
            self.message_history.pop(0)
        
        # Notify subscribers
        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                try:
                    callback(topic, payload)
                except Exception as e:
                    print(f"Error in subscriber callback: {e}")
        
        return True
    
    def subscribe(self, topic: str, callback: Callable) -> bool:
        """
        Subscribe to topic (simulated MQTT subscribe)
        """
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        
        self.subscribers[topic].append(callback)
        return True
    
    def unsubscribe(self, topic: str, callback: Callable) -> bool:
        """
        Unsubscribe from topic
        """
        if topic in self.subscribers:
            if callback in self.subscribers[topic]:
                self.subscribers[topic].remove(callback)
                return True
        return False
    
    # Convenience methods for cart events
    
    def publish_scan_event(self, cart_id: int, product_id: int, barcode: str):
        """Publish item scan event"""
        self.publish(
            f"cart/{cart_id}/scan",
            {
                "event_type": "item_scanned",
                "cart_id": cart_id,
                "product_id": product_id,
                "barcode": barcode
            }
        )
    
    def publish_camera_event(self, cart_id: int, detected_objects: list):
        """Publish camera detection event"""
        self.publish(
            f"cart/{cart_id}/camera",
            {
                "event_type": "camera_detection",
                "cart_id": cart_id,
                "detected_objects": detected_objects,
                "object_count": len(detected_objects)
            }
        )
    
    def publish_alert_event(self, cart_id: int, alert_type: str, message: str, severity: str):
        """Publish alert event"""
        self.publish(
            f"cart/{cart_id}/alert",
            {
                "event_type": "alert",
                "cart_id": cart_id,
                "alert_type": alert_type,
                "message": message,
                "severity": severity
            }
        )
    
    def publish_payment_event(self, cart_id: int, transaction_id: str, amount: float, status: str):
        """Publish payment event"""
        self.publish(
            f"cart/{cart_id}/payment",
            {
                "event_type": "payment",
                "cart_id": cart_id,
                "transaction_id": transaction_id,
                "amount": amount,
                "status": status
            }
        )
    
    def publish_cart_update(self, cart_id: int, total: float, item_count: int):
        """Publish cart update event"""
        self.publish(
            f"cart/{cart_id}/update",
            {
                "event_type": "cart_updated",
                "cart_id": cart_id,
                "total": total,
                "item_count": item_count
            }
        )
    
    def get_message_history(self, topic: Optional[str] = None, limit: int = 100) -> list:
        """Get message history for debugging"""
        messages = self.message_history
        if topic:
            messages = [m for m in messages if m["topic"] == topic]
        return messages[-limit:]


# Global IoT service instance
iot_service = IoTService()
