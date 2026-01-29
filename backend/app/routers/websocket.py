"""
WebSocket Router for Real-Time Fraud Detection
Handles WebSocket endpoints and real-time communication
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.websockets.connection_manager import get_connection_manager
import uuid
import json


router = APIRouter()


@router.websocket("/ws/fraud-alerts")
async def websocket_fraud_alerts(
    websocket: WebSocket,
    client_id: str = Query(default=None, description="Optional client ID")
):
    """
    WebSocket endpoint for real-time fraud alerts
    
    Usage:
        ws://localhost:8000/api/ws/fraud-alerts?client_id=user123
    
    Message Types Received:
        - {"type": "subscribe", "room": "high_risk_alerts"}
        - {"type": "unsubscribe", "room": "high_risk_alerts"}
        - {"type": "ping"}
    
    Message Types Sent:
        - {"type": "connection", "status": "connected", ...}
        - {"type": "fraud_alert", "fraud_probability": 0.85, ...}
        - {"type": "analysis_progress", "progress": 50, ...}
        - {"type": "pong"}
    """
    manager = get_connection_manager()
    
    # Generate client ID if not provided
    if not client_id:
        client_id = f"client_{uuid.uuid4().hex[:8]}"
    
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                message_type = message.get("type")
                
                # Handle different message types
                if message_type == "ping":
                    # Respond to ping with pong
                    await manager.send_personal_message(
                        {"type": "pong", "timestamp": message.get("timestamp")},
                        client_id
                    )
                
                elif message_type == "subscribe":
                    # Subscribe to a room
                    room = message.get("room")
                    if room:
                        manager.join_room(client_id, room)
                        await manager.send_personal_message(
                            {
                                "type": "subscribed",
                                "room": room,
                                "message": f"Subscribed to {room}"
                            },
                            client_id
                        )
                
                elif message_type == "unsubscribe":
                    # Unsubscribe from a room
                    room = message.get("room")
                    if room:
                        manager.leave_room(client_id, room)
                        await manager.send_personal_message(
                            {
                                "type": "unsubscribed",
                                "room": room,
                                "message": f"Unsubscribed from {room}"
                            },
                            client_id
                        )
                
                elif message_type == "get_stats":
                    # Send connection statistics
                    stats = manager.get_stats()
                    await manager.send_personal_message(
                        {
                            "type": "stats",
                            "data": stats
                        },
                        client_id
                    )
                
                else:
                    # Unknown message type
                    await manager.send_personal_message(
                        {
                            "type": "error",
                            "message": f"Unknown message type: {message_type}"
                        },
                        client_id
                    )
            
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    {
                        "type": "error",
                        "message": "Invalid JSON format"
                    },
                    client_id
                )
    
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        print(f"🔌 Client {client_id} disconnected")


@router.websocket("/ws/analysis/{analysis_id}")
async def websocket_analysis_progress(
    websocket: WebSocket,
    analysis_id: str,
    client_id: str = Query(default=None, description="Optional client ID")
):
    """
    WebSocket endpoint for tracking specific analysis progress
    
    Usage:
        ws://localhost:8000/api/ws/analysis/abc123?client_id=user123
    
    This endpoint is used for long-running analyses to provide
    real-time progress updates to the client.
    """
    manager = get_connection_manager()
    
    # Generate client ID if not provided
    if not client_id:
        client_id = f"client_{uuid.uuid4().hex[:8]}"
    
    await manager.connect(websocket, client_id)
    
    # Join analysis-specific room
    room = f"analysis_{analysis_id}"
    manager.join_room(client_id, room)
    
    try:
        while True:
            # Keep connection alive and handle messages
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                message_type = message.get("type")
                
                if message_type == "ping":
                    await manager.send_personal_message(
                        {"type": "pong", "timestamp": message.get("timestamp")},
                        client_id
                    )
            
            except json.JSONDecodeError:
                pass
    
    except WebSocketDisconnect:
        manager.leave_room(client_id, room)
        manager.disconnect(client_id)
        print(f"🔌 Client {client_id} disconnected from analysis {analysis_id}")


@router.get("/ws/stats")
async def get_websocket_stats():
    """
    Get WebSocket connection statistics
    
    Returns:
        Connection statistics including total connections and active rooms
    """
    manager = get_connection_manager()
    return {
        "status": "success",
        "data": manager.get_stats()
    }
