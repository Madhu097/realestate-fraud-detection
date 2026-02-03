"""
Application Configuration and Constants
Centralized configuration for the Truth in Listings API
"""
import os
from typing import List
from pydantic_settings import BaseSettings


# ============================================================
# APPLICATION CONSTANTS
# ============================================================

class AppConstants:
    """Application-wide constants"""
    
    # Application Info
    APP_NAME = "Truth in Listings"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Backend API for Truth in Listings - Fraud Detection System"
    
    # API Configuration
    API_PREFIX = "/api"
    DOCS_URL = "/docs"
    REDOC_URL = "/redoc"
    
    # CORS Origins (Development)
    CORS_ORIGINS = [
        "http://localhost:5173",  # Vite dev server (primary)
        "http://localhost:3000",  # Alternative frontend port
        "http://127.0.0.1:5173",  # Alternative localhost
        "http://127.0.0.1:3000",  # Alternative localhost
        "http://localhost:8000",  # Backend itself (for testing)
        "http://127.0.0.1:8000",  # Backend alternative
        "https://realestate-fraud-frontend.vercel.app",  # Vercel production
        "https://*.vercel.app",  # All Vercel preview deployments
    ]
    
    # File Upload Configuration
    UPLOAD_DIR = "app/uploads"
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB
    ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
    
    # Dataset Configuration
    DATASET_PATH = "app/data/real_estate.csv"
    
    # Database Configuration
    DATABASE_URL = "sqlite:///./sql_app.db"


# ============================================================
# FRAUD DETECTION CONSTANTS
# ============================================================

class FraudConstants:
    """Fraud detection module constants"""
    
    # Fusion Weights
    FUSION_WEIGHTS = {
        'price': 0.30,      # 30% - Price is a strong fraud indicator
        'image': 0.25,      # 25% - Image reuse is highly suspicious
        'text': 0.25,       # 25% - Text manipulation is common
        'location': 0.20    # 20% - Location fraud is detectable but less common
    }
    
    # Fraud Type Threshold
    FRAUD_TYPE_THRESHOLD = 0.6  # Only include fraud types with score > 0.6
    
    # Module-Specific Thresholds
    PRICE_FRAUD_THRESHOLD = 2.0  # Z-score threshold
    TEXT_FRAUD_THRESHOLD = 0.6   # Text fraud score threshold
    LOCATION_FRAUD_THRESHOLD = 50  # Distance threshold in km
    
    # Text Fraud Keywords
    URGENCY_KEYWORDS = [
        "urgent", "hurry", "limited time", "act now", "don't miss",
        "last chance", "today only", "immediate", "quick sale"
    ]
    
    SCAM_KEYWORDS = [
        "guaranteed", "risk-free", "100% safe", "no questions asked",
        "cash only", "wire transfer", "advance payment", "deposit now",
        "too good to be true", "once in a lifetime"
    ]
    
    EXAGGERATION_KEYWORDS = [
        "luxury", "premium", "exclusive", "world-class", "best",
        "amazing", "incredible", "unbelievable", "perfect", "ultimate"
    ]


# ============================================================
# VALIDATION CONSTANTS
# ============================================================

class ValidationConstants:
    """Input validation constants"""
    
    # String Length Limits
    MAX_TITLE_LENGTH = 500
    MAX_DESCRIPTION_LENGTH = 5000
    MAX_CITY_LENGTH = 100
    MAX_LOCALITY_LENGTH = 200
    
    # Numeric Limits
    MIN_PRICE = 0
    MAX_PRICE = 1_000_000_000_000  # 1 trillion
    MIN_AREA = 0
    MAX_AREA = 1_000_000  # 1 million sqft
    
    # Coordinate Limits
    MIN_LATITUDE = -90
    MAX_LATITUDE = 90
    MIN_LONGITUDE = -180
    MAX_LONGITUDE = 180


# ============================================================
# ERROR MESSAGES
# ============================================================

class ErrorMessages:
    """Standardized error messages"""
    
    # Validation Errors
    MISSING_LISTING_DATA = "listing_data is required for analysis"
    EMPTY_TITLE = "Title is required and cannot be empty"
    EMPTY_DESCRIPTION = "Description is required and cannot be empty"
    EMPTY_CITY = "City is required and cannot be empty"
    EMPTY_LOCALITY = "Locality is required and cannot be empty"
    
    INVALID_PRICE = "Price must be a positive number"
    ZERO_PRICE = "Price cannot be zero"
    PRICE_TOO_HIGH = "Price seems unreasonably high. Please verify the amount."
    
    INVALID_AREA = "Area must be a positive number"
    ZERO_AREA = "Area cannot be zero"
    AREA_TOO_LARGE = "Area seems unreasonably large. Please verify the measurement."
    
    INVALID_LATITUDE = "Latitude must be between -90 and 90"
    INVALID_LONGITUDE = "Longitude must be between -180 and 180"
    
    TITLE_TOO_LONG = f"Title is too long (maximum {ValidationConstants.MAX_TITLE_LENGTH} characters)"
    DESCRIPTION_TOO_LONG = f"Description is too long (maximum {ValidationConstants.MAX_DESCRIPTION_LENGTH} characters)"
    
    # Service Errors
    DATASET_NOT_LOADED = "Fraud detection service unavailable. Dataset not loaded."
    ANALYSIS_FAILED = "Failed to analyze listing. Please try again."
    
    # File Upload Errors
    NO_FILE_PROVIDED = "No file was provided"
    INVALID_FILE_TYPE = "Invalid file type. Allowed types: {allowed_types}"
    FILE_TOO_LARGE = f"File size exceeds maximum allowed size ({AppConstants.MAX_UPLOAD_SIZE // (1024*1024)} MB)"
    FILE_SAVE_FAILED = "Failed to save uploaded file"
    
    # Database Errors
    DATABASE_ERROR = "Database operation failed"
    RECORD_NOT_FOUND = "Record not found"


# ============================================================
# SUCCESS MESSAGES
# ============================================================

class SuccessMessages:
    """Standardized success messages"""
    
    ANALYSIS_COMPLETE = "Fraud analysis completed successfully"
    FILE_UPLOADED = "File uploaded successfully"
    RECORD_SAVED = "Record saved successfully"
    RECORD_DELETED = "Record deleted successfully"


# ============================================================
# ENVIRONMENT SETTINGS
# ============================================================

class Settings(BaseSettings):
    """
    Environment-based settings
    Loads from .env file if present
    """
    
    # Application Settings
    app_name: str = AppConstants.APP_NAME
    app_version: str = AppConstants.APP_VERSION
    debug: bool = False
    
    # Database Settings
    database_url: str = AppConstants.DATABASE_URL
    
    # CORS Settings - Allow string or list for flexibility
    cors_origins: str | List[str] = AppConstants.CORS_ORIGINS
    
    # File Upload Settings
    upload_dir: str = AppConstants.UPLOAD_DIR
    max_upload_size: int = AppConstants.MAX_UPLOAD_SIZE
    
    # Dataset Settings
    dataset_path: str = AppConstants.DATASET_PATH
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"  # Ignore extra fields
    }
    
    @property
    def get_cors_origins(self) -> List[str]:
        """Convert CORS origins to list format"""
        if isinstance(self.cors_origins, str):
            if self.cors_origins == "*":
                return ["*"]
            # Split by comma if multiple origins
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins


# Create settings instance
settings = Settings()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_app_info() -> dict:
    """Get application information"""
    return {
        "name": AppConstants.APP_NAME,
        "version": AppConstants.APP_VERSION,
        "description": AppConstants.APP_DESCRIPTION
    }


def get_fraud_weights() -> dict:
    """Get fraud detection fusion weights"""
    return FraudConstants.FUSION_WEIGHTS.copy()


def get_validation_limits() -> dict:
    """Get validation limits"""
    return {
        "title_max_length": ValidationConstants.MAX_TITLE_LENGTH,
        "description_max_length": ValidationConstants.MAX_DESCRIPTION_LENGTH,
        "max_price": ValidationConstants.MAX_PRICE,
        "max_area": ValidationConstants.MAX_AREA,
    }
