"""
WebSocket Connection Manager
Manages WebSocket connections, rooms, and message broadcasting
"""
from fastapi import WebSocket
from typing import Dict, Set, List
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections and broadcasting"""
    
    def __init__(self):
        # Active connections: {client_id: websocket}
        self.active_connections: Dict[str, WebSocket] = {}
        # Rooms: {room_name: set of client_ids}
        self.rooms: Dict[str, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept and store a new WebSocket connection"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected. Total connections: {len(self.active_connections)}")
        
        # Send connection confirmation
        await self.send_personal_message(
            {
                "type": "connection",
                "status": "connected",
                "client_id": client_id,
                "message": "Successfully connected to fraud detection system"
            },
            client_id
        )
    
    def disconnect(self, client_id: str):
        """Remove a WebSocket connection"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            # Remove from all rooms
            for room in self.rooms.values():
                room.discard(client_id)
            logger.info(f"Client {client_id} disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: dict, client_id: str):
        """Send a message to a specific client"""
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_json(message)
            except Exception as e:
                logger.error(f"Failed to send message to {client_id}: {e}")
                self.disconnect(client_id)
    
    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients"""
        disconnected_clients = []
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Failed to broadcast to {client_id}: {e}")
                disconnected_clients.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect(client_id)
    
    def join_room(self, client_id: str, room: str):
        """Add a client to a room"""
        if room not in self.rooms:
            self.rooms[room] = set()
        self.rooms[room].add(client_id)
        logger.info(f"Client {client_id} joined room: {room}")
    
    def leave_room(self, client_id: str, room: str):
        """Remove a client from a room"""
        if room in self.rooms:
            self.rooms[room].discard(client_id)
            if not self.rooms[room]:  # Remove empty rooms
                del self.rooms[room]
            logger.info(f"Client {client_id} left room: {room}")
    
    async def broadcast_to_room(self, message: dict, room: str):
        """Broadcast a message to all clients in a room"""
        if room not in self.rooms:
            return
        
        disconnected_clients = []
        for client_id in self.rooms[room]:
            if client_id in self.active_connections:
                try:
                    await self.active_connections[client_id].send_json(message)
                except Exception as e:
                    logger.error(f"Failed to send to {client_id} in room {room}: {e}")
                    disconnected_clients.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect(client_id)
    
    def get_room_clients(self, room: str) -> List[str]:
        """Get list of client IDs in a room"""
        return list(self.rooms.get(room, set()))
    
    def get_client_count(self) -> int:
        """Get total number of connected clients"""
        return len(self.active_connections)


# Global connection manager instance
_connection_manager = None


def get_connection_manager() -> ConnectionManager:
    """Get or create the global connection manager instance"""
    global _connection_manager
    if _connection_manager is None:
        _connection_manager = ConnectionManager()
    return _connection_manager
