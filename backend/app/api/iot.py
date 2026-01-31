"""
IoT Events API endpoints
"""
from fastapi import APIRouter, Query
from typing import Optional
from app.services.iot_service import iot_service

router = APIRouter(prefix="/iot", tags=["iot"])


@router.get("/messages")
def get_iot_messages(
    topic: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Get IoT message history (for debugging/monitoring)
    """
    messages = iot_service.get_message_history(topic=topic, limit=limit)
    return {
        "count": len(messages),
        "messages": messages
    }
