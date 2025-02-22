from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1.api import api_router
from app.api.errors.http_error import http_error_handler
from starlette.exceptions import HTTPException
from app.middleware.logging import logging_middleware
from app.monitoring.prometheus import metrics_middleware
from app.middleware.version import version_middleware
import uvicorn

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Middleware
app.middleware("http")(logging_middleware)
app.middleware("http")(metrics_middleware)
app.middleware("http")(version_middleware)

# Exception handlers
app.add_exception_handler(HTTPException, http_error_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# API routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)