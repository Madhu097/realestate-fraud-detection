"""
Truth in Listings - FastAPI Backend
Main application entry point with improved error handling and configuration
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from app.config import AppConstants, settings, get_app_info
from app.schemas import HealthCheckResponse, DetailedHealthCheckResponse
from app.exceptions import (
    BaseAPIException,
    base_api_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from app.routers import analyze, ml_analyze, image_upload, image_fraud_analysis, history, websocket
from app.database import engine
from app import models

# ============================================================
# DATABASE INITIALIZATION
# ============================================================

# Create database tables
models.Base.metadata.create_all(bind=engine)

# ============================================================
# APPLICATION INITIALIZATION
# ============================================================

app = FastAPI(
    title=AppConstants.APP_NAME,
    description=AppConstants.APP_DESCRIPTION,
    version=AppConstants.APP_VERSION,
    docs_url=AppConstants.DOCS_URL,
    redoc_url=AppConstants.REDOC_URL
)

# ============================================================
# MIDDLEWARE CONFIGURATION
# ============================================================

# CORS Middleware
# Allow specific origins for production and development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://realestate-fraud-frontend.vercel.app",
        "https://*.vercel.app",  # Allow all Vercel preview deployments
    ],
    allow_credentials=False,  # Keep False for security
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# ============================================================
# EXCEPTION HANDLERS
# ============================================================

# Register custom exception handlers
app.add_exception_handler(BaseAPIException, base_api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# ============================================================
# ROUTER REGISTRATION
# ============================================================

# Include routers with API prefix
app.include_router(
    analyze.router,
    prefix=AppConstants.API_PREFIX,
    tags=["Fraud Analysis"]
)

app.include_router(
    ml_analyze.router,
    prefix=AppConstants.API_PREFIX,
    tags=["ML Bulk Analysis"]
)

app.include_router(
    image_upload.router,
    prefix=AppConstants.API_PREFIX,
    tags=["Image Upload"]
)

app.include_router(
    image_fraud_analysis.router,
    prefix=AppConstants.API_PREFIX,
    tags=["Image Fraud Detection"]
)

app.include_router(
    history.router,
    prefix=AppConstants.API_PREFIX,
    tags=["Analysis History"]
)

# WebSocket router for real-time features
app.include_router(
    websocket.router,
    prefix=AppConstants.API_PREFIX,
    tags=["Real-Time WebSocket"]
)

# ============================================================
# HEALTH CHECK ENDPOINTS
# ============================================================

@app.api_route(
    "/",
    methods=["GET", "HEAD"],
    tags=["Health Check"],
    summary="Root endpoint",
    description="Simple root endpoint for uptime monitoring"
)
async def root():
    """
    Root endpoint - Simple response for monitoring services
    Supports both GET and HEAD methods for uptime monitoring
    
    Returns:
        dict: Simple status message
    """
    return {
        "status": "ok",
        "service": "Real Estate Fraud Detection API",
        "message": "Service is running"
    }


@app.api_route(
    "/api",
    methods=["GET", "HEAD"],
    response_model=HealthCheckResponse,
    tags=["Health Check"],
    summary="API health check",
    description="Returns the basic health status of the API"
)
async def api_health_check() -> HealthCheckResponse:
    """
    API health check endpoint
    
    Returns:
        HealthCheckResponse: Basic health status
    """
    app_info = get_app_info()
    return HealthCheckResponse(
        status="healthy",
        service=app_info["name"],
        version=app_info["version"],
        message="API is running successfully"
    )


@app.api_route(
    "/health",
    methods=["GET", "HEAD"],
    response_model=DetailedHealthCheckResponse,
    tags=["Health Check"],
    summary="Detailed health check",
    description="Returns detailed health status with available endpoints"
)
async def detailed_health_check() -> DetailedHealthCheckResponse:
    """
    Detailed health check endpoint
    
    Returns:
        DetailedHealthCheckResponse: Detailed health status with endpoints
    """
    app_info = get_app_info()
    return DetailedHealthCheckResponse(
        status="healthy",
        service=app_info["name"],
        version=app_info["version"],
        message="API is running successfully",
        endpoints={
            "health": "/health",
            "docs": AppConstants.DOCS_URL,
            "redoc": AppConstants.REDOC_URL,
            "analyze": f"{AppConstants.API_PREFIX}/analyze",
            "upload": f"{AppConstants.API_PREFIX}/upload",
            "history": f"{AppConstants.API_PREFIX}/history"
        }
    )


# ============================================================
# STARTUP/SHUTDOWN EVENTS
# ============================================================

@app.on_event("startup")
async def startup_event():
    """
    Application startup event
    Perform initialization tasks
    """
    print("=" * 80)
    print(f"  {AppConstants.APP_NAME} - Backend API")
    print(f"  Version: {AppConstants.APP_VERSION}")
    print("=" * 80)
    print(f"✅ Application started successfully")
    print(f"📚 API Documentation: {AppConstants.DOCS_URL}")
    print(f"🔍 ReDoc Documentation: {AppConstants.REDOC_URL}")
    print("=" * 80)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event
    Perform cleanup tasks
    """
    print("=" * 80)
    print(f"  {AppConstants.APP_NAME} - Shutting down")
    print("=" * 80)
    print("✅ Application shut down successfully")
    print("=" * 80)
