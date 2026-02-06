"""
Custom exceptions and error handlers for the Diet Planner API.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)


class DietServiceException(Exception):
    """Base exception for diet service errors."""
    
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(DietServiceException):
    """Exception for validation errors."""
    pass


class CalculationException(DietServiceException):
    """Exception for calculation errors."""
    pass


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """
    Handle Pydantic validation errors.
    
    Args:
        request: The FastAPI request object
        exc: The validation exception
        
    Returns:
        JSONResponse with standardized error format
    """
    logger.error(f"Validation error: {exc.errors()}")
    
    errors = exc.errors()
    error_details = {}
    
    if errors:
        first_error = errors[0]
        error_details = {
            "field": " -> ".join(str(loc) for loc in first_error.get("loc", [])),
            "issue": first_error.get("msg", "Invalid value"),
            "type": first_error.get("type", "validation_error")
        }
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "ValidationError",
            "message": "Invalid input data provided",
            "details": error_details
        }
    )


async def diet_service_exception_handler(
    request: Request,
    exc: DietServiceException
) -> JSONResponse:
    """
    Handle custom diet service exceptions.
    
    Args:
        request: The FastAPI request object
        exc: The diet service exception
        
    Returns:
        JSONResponse with standardized error format
    """
    logger.error(f"Diet service error: {exc.message}")
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details
        }
    )


async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """
    Handle unexpected exceptions.
    
    Args:
        request: The FastAPI request object
        exc: The exception
        
    Returns:
        JSONResponse with standardized error format
    """
    logger.exception(f"Unexpected error: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "InternalServerError",
            "message": "An unexpected error occurred. Please try again later.",
            "details": {}
        }
    )
