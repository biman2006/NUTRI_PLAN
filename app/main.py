"""
Diet Planner API - Professional FastAPI Application

A comprehensive nutrition planning API that provides personalized diet plans,
BMI calculations, and macro-nutrient recommendations based on fitness goals.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.routes import router
from app.exceptions import (
    validation_exception_handler,
    diet_service_exception_handler,
    general_exception_handler,
    DietServiceException
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    """
    # Startup
    logger.info("🚀 Starting Diet Planner API...")
    logger.info(f"Version: {settings.app_version}")
    logger.info(f"Environment: {'Development' if settings.debug else 'Production'}")
    yield
    # Shutdown
    logger.info("👋 Shutting down Diet Planner API...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Diet Planning",
            "description": "Endpoints for generating personalized nutrition plans and meal recommendations"
        }
    ]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(DietServiceException, diet_service_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(router)

logger.info("✅ Application setup complete")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )



from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
