"""
Analyze Router
Handles analysis-related endpoints

FROZEN LISTING DATA SCHEMA:
This schema is used by all fraud modules, database, frontend forms, and evaluation.
{
  "title": "string",
  "description": "string",
  "price": 0,
  "area_sqft": 0,
  "city": "string",
  "locality": "string",
  "latitude": 0.0,
  "longitude": 0.0
}
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

# Import fraud detection services
from app.services.price_fraud import detect_price_fraud
from app.services.text_fraud import detect_text_fraud
from app.services.location_fraud import detect_location_fraud
from app.services.external_location_verification import verify_location_with_external_apis
from app.services.amenity_verification import verify_amenity_claims
from app.services.fusion import fuse_fraud_signals
from app.utils.data_loader import load_dataset

router = APIRouter()

# Load dataset once at startup
try:
    dataset = load_dataset()
    print(f"✅ Dataset loaded: {len(dataset)} properties")
except Exception as e:
    print(f"⚠️ Warning: Could not load dataset: {e}")
    dataset = None



class ListingData(BaseModel):
    """
    FROZEN LISTING DATA SCHEMA
    This schema is used by all fraud modules, database, frontend forms, and evaluation.
    DO NOT MODIFY without updating all dependent systems.
    """
    title: str = Field(..., description="The listing title/headline")
    description: str = Field(..., description="Detailed description of the property")
    price: float = Field(..., ge=0, description="Price in the local currency")
    area_sqft: float = Field(..., ge=0, description="Area in square feet")
    city: str = Field(..., description="City name")
    locality: str = Field(..., description="Specific locality/neighborhood")
    latitude: float = Field(..., ge=-90, le=90, description="Geographic latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Geographic longitude coordinate")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Spacious 3BHK Apartment in Prime Location",
                "description": "Beautiful 3BHK apartment with modern amenities, parking, and great view",
                "price": 5000000,
                "area_sqft": 1500,
                "city": "Mumbai",
                "locality": "Andheri West",
                "latitude": 19.1334,
                "longitude": 72.8291
            }
        }


class AnalyzeRequest(BaseModel):
    """Request model for analysis endpoint"""
    listing_id: Optional[str] = None
    listing_url: Optional[str] = None
    listing_data: Optional[ListingData] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "listing_id": "12345",
                "listing_url": "https://example.com/listing/12345",
                "listing_data": {
                    "title": "Spacious 3BHK Apartment in Prime Location",
                    "description": "Beautiful 3BHK apartment with modern amenities",
                    "price": 5000000,
                    "area_sqft": 1500,
                    "city": "Mumbai",
                    "locality": "Andheri West",
                    "latitude": 19.1334,
                    "longitude": 72.8291
                }
            }
        }


class FraudReport(BaseModel):
    """
    Fraud Report Response Model
    This is the standardized response format for fraud analysis.
    """
    fraud_probability: float = Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="Probability of fraud (0.0 = no fraud, 1.0 = definite fraud)"
    )
    fraud_types: list[str] = Field(
        default_factory=list,
        description="List of detected fraud types (e.g., 'price_manipulation', 'fake_location')"
    )
    explanations: list[str] = Field(
        default_factory=list,
        description="Human-readable explanations for detected fraud indicators"
    )
    module_scores: Optional[dict] = Field(
        default_factory=dict,
        description="Individual fraud scores for each module (for visualization)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "fraud_probability": 0.75,
                "fraud_types": ["price_manipulation", "suspicious_description"],
                "explanations": [
                    "Price is 40% below market average for this locality",
                    "Description contains urgency keywords commonly used in scams"
                ]
            }
        }


@router.post("/analyze", response_model=FraudReport)
async def analyze_listing(request: AnalyzeRequest):
    """
    Analyze a listing for potential fraud (DUMMY LOGIC)
    
    This endpoint accepts listing data and returns a fraud analysis report.
    Currently returns dummy data with correct structure.
    
    This will become the single entry point for all fraud detection modules.
    
    Args:
        request: AnalyzeRequest containing listing information
        
    Returns:
        FraudReport with fraud probability, types, and explanations
        
    Raises:
        HTTPException: If validation fails
    """
    # VALIDATION 1: Check if listing_data is provided
    if not request.listing_data:
        raise HTTPException(
            status_code=400,
            detail="listing_data is required for analysis"
        )
    
    listing = request.listing_data
    
    # VALIDATION 2: Check required string fields are not empty
    if not listing.title or not listing.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required and cannot be empty"
        )
    
    if not listing.description or not listing.description.strip():
        raise HTTPException(
            status_code=400,
            detail="Description is required and cannot be empty"
        )
    
    if not listing.city or not listing.city.strip():
        raise HTTPException(
            status_code=400,
            detail="City is required and cannot be empty"
        )
    
    if not listing.locality or not listing.locality.strip():
        raise HTTPException(
            status_code=400,
            detail="Locality is required and cannot be empty"
        )
    
    # VALIDATION 3: Check numeric fields are valid
    if listing.price < 0:
        raise HTTPException(
            status_code=400,
            detail="Price must be a positive number"
        )
    
    if listing.price == 0:
        raise HTTPException(
            status_code=400,
            detail="Price cannot be zero"
        )
    
    if listing.area_sqft < 0:
        raise HTTPException(
            status_code=400,
            detail="Area must be a positive number"
        )
    
    if listing.area_sqft == 0:
        raise HTTPException(
            status_code=400,
            detail="Area cannot be zero"
        )
    
    # VALIDATION 4: Check coordinate ranges
    if listing.latitude < -90 or listing.latitude > 90:
        raise HTTPException(
            status_code=400,
            detail=f"Latitude must be between -90 and 90 (got {listing.latitude})"
        )
    
    if listing.longitude < -180 or listing.longitude > 180:
        raise HTTPException(
            status_code=400,
            detail=f"Longitude must be between -180 and 180 (got {listing.longitude})"
        )
    
    # VALIDATION 5: Check for reasonable values
    if listing.price > 1000000000000:  # 1 trillion
        raise HTTPException(
            status_code=400,
            detail="Price seems unreasonably high. Please verify the amount."
        )
    
    if listing.area_sqft > 1000000:  # 1 million sqft
        raise HTTPException(
            status_code=400,
            detail="Area seems unreasonably large. Please verify the measurement."
        )
    
    # VALIDATION 6: Check string lengths
    if len(listing.title) > 500:
        raise HTTPException(
            status_code=400,
            detail="Title is too long (maximum 500 characters)"
        )
    
    if len(listing.description) > 5000:
        raise HTTPException(
            status_code=400,
            detail="Description is too long (maximum 5000 characters)"
        )
    
    # All validations passed!
    
    # Check if dataset is available
    if dataset is None:
        raise HTTPException(
            status_code=503,
            detail="Fraud detection service unavailable. Dataset not loaded."
        )
    
    # ============================================================
    # FRAUD DETECTION MODULE 1: PRICE ANALYSIS
    # ============================================================
    price_score, price_explanation = detect_price_fraud(
        listing_price=listing.price,
        locality=listing.locality,
        city=listing.city,
        df=dataset
    )
    
    # ============================================================
    # FRAUD DETECTION MODULE 2: TEXT ANALYSIS
    # ============================================================
    text_score, text_explanations = detect_text_fraud(
        title=listing.title,
        description=listing.description,
        save_to_corpus=True
    )
    
    # ============================================================
    # FRAUD DETECTION MODULE 3: LOCATION ANALYSIS
    # ============================================================
    # Note: City is required for accurate location verification
    location_score, location_explanation = detect_location_fraud(
        locality=listing.locality,
        latitude=listing.latitude,
        longitude=listing.longitude,
        city=listing.city,
        price=listing.price  # For price-location sanity check
    )
    
    # ============================================================
    # FRAUD DETECTION MODULE 4: EXTERNAL LOCATION VERIFICATION (NEW)
    # ============================================================
    # Verify location using external APIs (Nominatim, BigDataCloud, etc.)
    try:
        external_location_score, external_location_explanation, _ = verify_location_with_external_apis(
            latitude=listing.latitude,
            longitude=listing.longitude,
            claimed_city=listing.city,
            claimed_locality=listing.locality
        )
    except Exception as e:
        print(f"External location verification failed: {e}")
        external_location_score = 0.0
        external_location_explanation = "External location verification unavailable."
    
    # ============================================================
    # FRAUD DETECTION MODULE 5: AMENITY VERIFICATION (NEW)
    # ============================================================
    # Verify amenity claims using Overpass API
    try:
        amenity_score, amenity_explanation, _ = verify_amenity_claims(
            title=listing.title,
            description=listing.description,
            latitude=listing.latitude,
            longitude=listing.longitude
        )
    except Exception as e:
        print(f"Amenity verification failed: {e}")
        amenity_score = 0.0
        amenity_explanation = "Amenity verification unavailable."
    
    # ============================================================
    # FRAUD DETECTION MODULE 6: IMAGE ANALYSIS (Placeholder)
    # ============================================================
    # TODO: Integrate image fraud detection when images are provided
    # For now, set to 0.0 (no image fraud detected)
    image_score = 0.0
    image_explanation = "Image fraud detection not yet integrated."
    
    # ============================================================
    # FUSION ENGINE: Combine all fraud signals
    # ============================================================
    # Use weighted fusion engine for explainable, deterministic combination
    # Weights: Price (25%), Image (20%), Text (20%), Location (15%), 
    #          External Location (15%), Amenity (5%)
    
    final_fraud_probability, fraud_types, explanations = fuse_fraud_signals(
        price_score=price_score,
        price_explanation=price_explanation,
        image_score=image_score,
        image_explanation=image_explanation,
        text_score=text_score,
        text_explanations=text_explanations,
        location_score=location_score,
        location_explanation=location_explanation,
        external_location_score=external_location_score,
        external_location_explanation=external_location_explanation,
        amenity_score=amenity_score,
        amenity_explanation=amenity_explanation
    )
    
    # Return fraud report
    return FraudReport(
        fraud_probability=final_fraud_probability,
        fraud_types=fraud_types,
        explanations=explanations,
        module_scores={
            "Price": price_score,
            "Image": image_score,
            "Text": text_score,
            "Location": location_score,
            "External Location": external_location_score,
            "Amenity": amenity_score
        }
    )


@router.get("/analyze/status")
async def get_analysis_status():
    """
    Get the status of the analysis service
    
    Returns:
        Service status information
    """
    dataset_status = "loaded" if dataset is not None else "not_loaded"
    return {
        "status": "operational" if dataset is not None else "degraded",
        "service": "Analysis Service",
        "message": f"Ready ({dataset_status})",
        "dataset_size": len(dataset) if dataset is not None else 0
    }
