from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import get_db, insert_notification
from app.routes.auth import router as auth_router
from app.utils.auth import get_current_user  # Assuming this exists
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

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

# Middleware to log API requests
@app.middleware("http")
async def api_tracking_middleware(request: Request, call_next):
    """Middleware to track API calls and store them in the database."""
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
    insert_notification(
        db,
        method=request.method,
        path=request.url.path,
        user_id=user_id,
        request_body=request_body.decode() if request_body else None,
        response_body=response_body.decode() if response_body else None,
        status_code=response.status_code,
        headers=str(headers),
        client_host=client_host,
        query_params=str(query_params)
    )

    # Reconstruct response
    return response

app.include_router(auth_router, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
