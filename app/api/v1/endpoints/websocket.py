from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from ....websockets.connection import manager
from ....api.deps import get_current_user
from ....models.user import User
from sqlalchemy.orm import Session
from ....api.deps import get_db
import json

router = APIRouter()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: int,
    db: Session = Depends(get_db)
):
    user = await get_current_user(db=db, token=client_id)
    await manager.connect(websocket, user.id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            # Handle different message types
            if message.get("type") == "chat":
                await manager.send_personal_message(
                    json.dumps({
                        "type": "chat",
                        "from": user.username,
                        "content": message.get("content")
                    }),
                    user.id
                )
    except WebSocketDisconnect:
        manager.disconnect(websocket, user.id)
        await manager.broadcast(f"Client #{client_id} left the chat")
