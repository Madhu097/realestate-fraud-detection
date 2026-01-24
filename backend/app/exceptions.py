"""
Exception Handlers and Error Utilities
Centralized error handling for the application
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from typing import Union
import traceback
import logging

from app.schemas import create_error_response, create_validation_error_response
from app.config import ErrorMessages


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================
# CUSTOM EXCEPTIONS
# ============================================================

class BaseAPIException(Exception):
    """Base exception for API errors"""
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "INTERNAL_ERROR",
        details: dict = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(BaseAPIException):
    """Validation error exception"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="VALIDATION_ERROR",
            details=details
        )


class DatasetNotFoundException(BaseAPIException):
    """Dataset not found exception"""
    def __init__(self, message: str = ErrorMessages.DATASET_NOT_LOADED):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="DATASET_NOT_LOADED"
        )


class AnalysisException(BaseAPIException):
    """Analysis failed exception"""
    def __init__(self, message: str = ErrorMessages.ANALYSIS_FAILED, details: dict = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="ANALYSIS_FAILED",
            details=details
        )


class FileUploadException(BaseAPIException):
    """File upload error exception"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="FILE_UPLOAD_ERROR",
            details=details
        )


class DatabaseException(BaseAPIException):
    """Database operation error exception"""
    def __init__(self, message: str = ErrorMessages.DATABASE_ERROR, details: dict = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="DATABASE_ERROR",
            details=details
        )


# ============================================================
# EXCEPTION HANDLERS
# ============================================================

async def base_api_exception_handler(request: Request, exc: BaseAPIException) -> JSONResponse:
    """
    Handler for custom API exceptions
    
    Args:
        request: FastAPI request object
        exc: Custom API exception
        
    Returns:
        JSON response with error details
    """
    logger.error(f"API Exception: {exc.message} | Code: {exc.error_code} | Path: {request.url.path}")
    
    response_data = create_error_response(
        message=exc.message,
        error_code=exc.error_code,
        details=exc.details if exc.details else None
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_data
    )


async def validation_exception_handler(
    request: Request,
    exc: Union[RequestValidationError, ValidationError]
) -> JSONResponse:
    """
    Handler for Pydantic validation errors
    
    Args:
        request: FastAPI request object
        exc: Validation error exception
        
    Returns:
        JSON response with validation error details
    """
    logger.warning(f"Validation Error: {request.url.path}")
    
    # Extract validation errors
    validation_errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        validation_errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    
    response_data = create_validation_error_response(
        message="Validation failed. Please check your input.",
        validation_errors=validation_errors
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response_data
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler for unexpected exceptions
    
    Args:
        request: FastAPI request object
        exc: Any exception
        
    Returns:
        JSON response with generic error message
    """
    logger.error(f"Unexpected Error: {str(exc)} | Path: {request.url.path}")
    logger.error(traceback.format_exc())
    
    response_data = create_error_response(
        message="An unexpected error occurred. Please try again later.",
        error_code="INTERNAL_ERROR",
        details={"error": str(exc)} if logger.level == logging.DEBUG else None
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response_data
    )


# ============================================================
# VALIDATION HELPERS
# ============================================================

def validate_listing_data(listing_data):
    """
    Validate listing data with detailed error messages
    
    Args:
        listing_data: ListingData object to validate
        
    Raises:
        ValidationException: If validation fails
    """
    from app.config import ValidationConstants, ErrorMessages
    
    errors = []
    
    # Validate title
    if not listing_data.title or not listing_data.title.strip():
        errors.append({
            "field": "title",
            "message": ErrorMessages.EMPTY_TITLE,
            "value": listing_data.title
        })
    elif len(listing_data.title) > ValidationConstants.MAX_TITLE_LENGTH:
        errors.append({
            "field": "title",
            "message": ErrorMessages.TITLE_TOO_LONG,
            "value": f"Length: {len(listing_data.title)}"
        })
    
    # Validate description
    if not listing_data.description or not listing_data.description.strip():
        errors.append({
            "field": "description",
            "message": ErrorMessages.EMPTY_DESCRIPTION,
            "value": listing_data.description
        })
    elif len(listing_data.description) > ValidationConstants.MAX_DESCRIPTION_LENGTH:
        errors.append({
            "field": "description",
            "message": ErrorMessages.DESCRIPTION_TOO_LONG,
            "value": f"Length: {len(listing_data.description)}"
        })
    
    # Validate city
    if not listing_data.city or not listing_data.city.strip():
        errors.append({
            "field": "city",
            "message": ErrorMessages.EMPTY_CITY,
            "value": listing_data.city
        })
    
    # Validate locality
    if not listing_data.locality or not listing_data.locality.strip():
        errors.append({
            "field": "locality",
            "message": ErrorMessages.EMPTY_LOCALITY,
            "value": listing_data.locality
        })
    
    # Validate price
    if listing_data.price < 0:
        errors.append({
            "field": "price",
            "message": ErrorMessages.INVALID_PRICE,
            "value": listing_data.price
        })
    elif listing_data.price == 0:
        errors.append({
            "field": "price",
            "message": ErrorMessages.ZERO_PRICE,
            "value": listing_data.price
        })
    elif listing_data.price > ValidationConstants.MAX_PRICE:
        errors.append({
            "field": "price",
            "message": ErrorMessages.PRICE_TOO_HIGH,
            "value": listing_data.price
        })
    
    # Validate area
    if listing_data.area_sqft < 0:
        errors.append({
            "field": "area_sqft",
            "message": ErrorMessages.INVALID_AREA,
            "value": listing_data.area_sqft
        })
    elif listing_data.area_sqft == 0:
        errors.append({
            "field": "area_sqft",
            "message": ErrorMessages.ZERO_AREA,
            "value": listing_data.area_sqft
        })
    elif listing_data.area_sqft > ValidationConstants.MAX_AREA:
        errors.append({
            "field": "area_sqft",
            "message": ErrorMessages.AREA_TOO_LARGE,
            "value": listing_data.area_sqft
        })
    
    # Validate coordinates
    if listing_data.latitude < ValidationConstants.MIN_LATITUDE or listing_data.latitude > ValidationConstants.MAX_LATITUDE:
        errors.append({
            "field": "latitude",
            "message": ErrorMessages.INVALID_LATITUDE,
            "value": listing_data.latitude
        })
    
    if listing_data.longitude < ValidationConstants.MIN_LONGITUDE or listing_data.longitude > ValidationConstants.MAX_LONGITUDE:
        errors.append({
            "field": "longitude",
            "message": ErrorMessages.INVALID_LONGITUDE,
            "value": listing_data.longitude
        })
    
    # If there are errors, raise ValidationException
    if errors:
        raise ValidationException(
            message="Validation failed. Please check your input.",
            details={"validation_errors": errors}
        )


# ============================================================
# SAFE EXECUTION WRAPPER
# ============================================================

def safe_execute(func, *args, error_message: str = "Operation failed", **kwargs):
    """
    Safely execute a function with error handling
    
    Args:
        func: Function to execute
        *args: Positional arguments for the function
        error_message: Error message if execution fails
        **kwargs: Keyword arguments for the function
        
    Returns:
        Function result
        
    Raises:
        AnalysisException: If execution fails
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Safe execution failed: {str(e)}")
        logger.error(traceback.format_exc())
        raise AnalysisException(
            message=error_message,
            details={"error": str(e)}
        )
