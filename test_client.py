import asyncio
import websockets
import json
from datetime import datetime

async def test_client():
    uri = "ws://localhost:8001/ws/notifications"
    print(f"Connecting to {uri}...")
    
    async with websockets.connect(uri) as websocket:
        print("Connected to notification service")
        
        try:
            while True:
                # Receive notification
                message = await websocket.recv()
                notification = json.loads(message)
                print(f"\nReceived notification: {notification}")
                
                # Send confirmation
                confirmation = {
                    "status": "received",
                    "notification_id": notification.get("id"),
                    "timestamp": str(datetime.utcnow())
                }
                await websocket.send(json.dumps(confirmation))
                print(f"Sent confirmation: {confirmation}")
                
        except websockets.ConnectionClosed:
            print("Connection closed")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting WebSocket test client...")
    asyncio.run(test_client())
