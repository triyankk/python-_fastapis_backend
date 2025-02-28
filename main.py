from fastapi import FastAPI, Request, Depends, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import get_db
from app.routes.auth import router as auth_router
from app.routes.notification import router as notification_router
from app.utils.auth import get_current_user  # Assuming this exists
from app.services.notification_service import insert_notification
from app.utils.error_handler import APIError, DatabaseError, handle_error, logger
import os
from dotenv import load_dotenv
from starlette.responses import Response
import json
import asyncio
import websockets

load_dotenv()

app = FastAPI()

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content=handle_error(exc)
    )

@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=handle_error(exc)
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=handle_error(exc)
    )

# Store connected WebSocket clients
websocket_clients = []

@app.get("/")
async def root():
    return {"message": "Welcome to DataViv API"}

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket endpoint for notifications
@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_clients.remove(websocket)

# Middleware to log API requests
@app.middleware("http")
async def api_tracking_middleware(request: Request, call_next):
    """Middleware to track API calls and store them in the database."""
    try:
        db: Session = next(get_db())

        # Get user info if authenticated
        user_id = None
        try:
            user = await get_current_user(request)  # Extract user from token
            user_id = user.id if user else None
        except:
            pass  # If user isn't authenticated, keep user_id as None

        # Get request details
        request_body = await request.body()
        headers = dict(request.headers)
        client_host = request.client.host
        query_params = dict(request.query_params)

        # Call the next middleware or endpoint
        response = await call_next(request)
        
        # Get response details
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        # Insert log into database
        await insert_notification(
            db,
            method=request.method,
            path=request.url.path,
            user_id=user_id,
            request_body=request_body.decode() if request_body else None,
            response_body=response_body.decode() if response_body else None,
            status_code=response.status_code,
            headers=headers,
            client_host=client_host,
            query_params=query_params
        )

        # Reconstruct response
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )
    except Exception as e:
        logger.error(f"Middleware error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=handle_error(e)
        )

# WebSocket client to connect to the notification web service
async def connect_to_notifications():
    uri = "ws://localhost:8001/ws/notifications"
    async with websockets.connect(uri) as websocket:
        print("Connected to notification service")
        try:
            while True:
                message = await websocket.recv()
                notification = json.loads(message)
                print(f"Received notification: {notification}")
                # Print confirmation message
                print("Notification received and processed successfully")
        except websockets.ConnectionClosed:
            print("Connection to notification service closed")

@app.on_event("startup")
async def startup_event():
    db: Session = next(get_db())
    try:
        await insert_notification(
            db,
            method="SYSTEM",
            path="/startup",
            user_id=None,
            request_body=None,
            response_body=json.dumps("Server started"),
            status_code=200,
            headers={},
            client_host="localhost",
            query_params={}
        )
    finally:
        db.close()
    asyncio.create_task(connect_to_notifications())

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(notification_router, prefix="/notifications", tags=["notifications"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
