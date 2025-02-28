import asyncio
import websockets
import json
from app.utils.error_handler import logger
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
from typing import Dict, List

# Store connected WebSocket clients with their status
class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[WebSocket, dict] = {}
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[websocket] = {
            "connected_at": datetime.utcnow(),
            "last_seen": datetime.utcnow(),
            "status": "connected"
        }
        logger.info(f"New WebSocket client connected. Total clients: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            del self.active_connections[websocket]
            logger.info(f"WebSocket client disconnected. Remaining clients: {len(self.active_connections)}")
    
    async def broadcast(self, message: str) -> List[dict]:
        delivery_status = []
        disconnected_clients = []
        
        for websocket in self.active_connections:
            try:
                await websocket.send_text(message)
                # Update last seen timestamp
                self.active_connections[websocket]["last_seen"] = datetime.utcnow()
                self.active_connections[websocket]["status"] = "active"
                delivery_status.append({
                    "status": "delivered",
                    "timestamp": str(datetime.utcnow())
                })
            except Exception as e:
                logger.error(f"Failed to send message to client: {e}")
                disconnected_clients.append(websocket)
                delivery_status.append({
                    "status": "failed",
                    "error": str(e),
                    "timestamp": str(datetime.utcnow())
                })
        
        # Clean up disconnected clients
        for client in disconnected_clients:
            self.disconnect(client)
        
        return delivery_status

    def get_status(self) -> List[dict]:
        return [{
            "connected_at": str(info["connected_at"]),
            "last_seen": str(info["last_seen"]),
            "status": info["status"]
        } for info in self.active_connections.values()]

# Create global WebSocket manager instance
manager = WebSocketManager()

async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Wait for client messages (confirmations)
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                logger.info(f"Received from client: {message}")
            except json.JSONDecodeError:
                logger.warning(f"Received invalid JSON from client: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# Example WebSocket client
async def example_client():
    uri = "ws://localhost:8001/ws/notifications"
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                logger.info(f"Client received: {data}")
                
                # Send confirmation
                await websocket.send(json.dumps({
                    "status": "received",
                    "timestamp": str(datetime.utcnow())
                }))
            except Exception as e:
                logger.error(f"Client error: {e}")
                break

if __name__ == "__main__":
    asyncio.run(example_client())
