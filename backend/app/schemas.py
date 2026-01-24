"""
Common Response Schemas
Standardized response models for consistent API responses
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


# ============================================================
# BASE RESPONSE MODELS
# ============================================================

class BaseResponse(BaseModel):
    """Base response model for all API responses"""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Human-readable message")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="Response timestamp (ISO 8601)")


class ErrorResponse(BaseResponse):
    """Standard error response"""
    success: bool = Field(default=False, description="Always False for errors")
    error_code: Optional[str] = Field(None, description="Machine-readable error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "message": "Validation failed",
                "error_code": "VALIDATION_ERROR",
                "details": {
                    "field": "price",
                    "issue": "Price cannot be zero"
                },
                "timestamp": "2026-01-20T10:00:00.000Z"
            }
        }


class SuccessResponse(BaseResponse):
    """Standard success response"""
    success: bool = Field(default=True, description="Always True for success")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data payload")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {
                    "id": "12345",
                    "status": "processed"
                },
                "timestamp": "2026-01-20T10:00:00.000Z"
            }
        }


# ============================================================
# HEALTH CHECK RESPONSES
# ============================================================

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status (healthy/unhealthy)")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    message: str = Field(..., description="Status message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "service": "Truth in Listings API",
                "version": "1.0.0",
                "message": "API is running successfully"
            }
        }


class DetailedHealthCheckResponse(HealthCheckResponse):
    """Detailed health check response with endpoints"""
    endpoints: Dict[str, str] = Field(..., description="Available API endpoints")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "service": "Truth in Listings API",
                "version": "1.0.0",
                "message": "API is running successfully",
                "endpoints": {
                    "health": "/health",
                    "docs": "/docs",
                    "analyze": "/api/analyze"
                }
            }
        }


# ============================================================
# FRAUD ANALYSIS RESPONSES
# ============================================================

class FraudAnalysisResponse(BaseResponse):
    """Fraud analysis response"""
    success: bool = Field(default=True)
    message: str = Field(default="Fraud analysis completed successfully")
    data: Dict[str, Any] = Field(..., description="Fraud analysis results")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Fraud analysis completed successfully",
                "data": {
                    "fraud_probability": 0.75,
                    "fraud_types": ["Price Fraud", "Text Fraud"],
                    "explanations": [
                        "Price is 40% below market average",
                        "Description contains urgency keywords"
                    ],
                    "module_scores": {
                        "Price": 0.85,
                        "Image": 0.0,
                        "Text": 0.70,
                        "Location": 0.15
                    }
                },
                "timestamp": "2026-01-20T10:00:00.000Z"
            }
        }


# ============================================================
# FILE UPLOAD RESPONSES
# ============================================================

class FileUploadResponse(BaseResponse):
    """File upload response"""
    success: bool = Field(default=True)
    message: str = Field(default="File uploaded successfully")
    data: Dict[str, Any] = Field(..., description="Upload details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "File uploaded successfully",
                "data": {
                    "filename": "property_image.jpg",
                    "file_path": "/uploads/abc123.jpg",
                    "file_size": 1024000,
                    "content_type": "image/jpeg"
                },
                "timestamp": "2026-01-20T10:00:00.000Z"
            }
        }


# ============================================================
# HISTORY RESPONSES
# ============================================================

class HistoryListResponse(BaseResponse):
    """History list response"""
    success: bool = Field(default=True)
    message: str = Field(default="History retrieved successfully")
    data: Dict[str, Any] = Field(..., description="History data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "History retrieved successfully",
                "data": {
                    "total": 10,
                    "items": [
                        {
                            "id": 1,
                            "title": "3BHK Apartment",
                            "fraud_probability": 0.75,
                            "timestamp": "2026-01-20T10:00:00"
                        }
                    ]
                },
                "timestamp": "2026-01-20T10:00:00.000Z"
            }
        }


# ============================================================
# VALIDATION RESPONSE
# ============================================================

class ValidationErrorDetail(BaseModel):
    """Validation error detail"""
    field: str = Field(..., description="Field name that failed validation")
    message: str = Field(..., description="Validation error message")
    value: Optional[Any] = Field(None, description="Invalid value provided")


class ValidationErrorResponse(ErrorResponse):
    """Validation error response with field details"""
    error_code: str = Field(default="VALIDATION_ERROR")
    validation_errors: List[ValidationErrorDetail] = Field(..., description="List of validation errors")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "message": "Validation failed",
                "error_code": "VALIDATION_ERROR",
                "validation_errors": [
                    {
                        "field": "price",
                        "message": "Price cannot be zero",
                        "value": 0
                    },
                    {
                        "field": "title",
                        "message": "Title is required and cannot be empty",
                        "value": ""
                    }
                ],
                "timestamp": "2026-01-20T10:00:00.000Z"
            }
        }


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def create_success_response(
    message: str,
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a standardized success response
    
    Args:
        message: Success message
        data: Optional data payload
        
    Returns:
        Standardized success response dictionary
    """
    response = {
        "success": True,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if data is not None:
        response["data"] = data
    
    return response


def create_error_response(
    message: str,
    error_code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a standardized error response
    
    Args:
        message: Error message
        error_code: Optional machine-readable error code
        details: Optional additional error details
        
    Returns:
        Standardized error response dictionary
    """
    response = {
        "success": False,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if error_code:
        response["error_code"] = error_code
    
    if details:
        response["details"] = details
    
    return response


def create_validation_error_response(
    message: str,
    validation_errors: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Create a standardized validation error response
    
    Args:
        message: General error message
        validation_errors: List of validation error details
        
    Returns:
        Standardized validation error response dictionary
    """
    return {
        "success": False,
        "message": message,
        "error_code": "VALIDATION_ERROR",
        "validation_errors": validation_errors,
        "timestamp": datetime.utcnow().isoformat()
    }
