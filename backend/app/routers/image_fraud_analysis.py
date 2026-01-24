"""
Image Fraud Analysis Router
Analyzes images for fraud detection
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.image_fraud import detect_image_fraud

router = APIRouter()


class ImageFraudRequest(BaseModel):
    """Request model for image fraud analysis"""
    image_paths: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_paths": [
                    "app/uploads/image1.jpg",
                    "app/uploads/image2.jpg"
                ]
            }
        }


class ImageFraudResponse(BaseModel):
    """Response model for image fraud analysis"""
    image_fraud_score: float
    duplicate_images: int
    explanation: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_fraud_score": 0.78,
                "duplicate_images": 3,
                "explanation": "Same image detected in multiple listings"
            }
        }


@router.post("/image-fraud", response_model=ImageFraudResponse)
async def analyze_image_fraud(request: ImageFraudRequest):
    """
    Analyze images for fraud (duplicate/reused images)
    
    Args:
        request: ImageFraudRequest with list of image paths
        
    Returns:
        ImageFraudResponse with fraud score and explanation
    """
    if not request.image_paths:
        raise HTTPException(
            status_code=400,
            detail="No image paths provided"
        )
    
    try:
        # Run image fraud detection
        fraud_score, duplicate_count, explanation = detect_image_fraud(
            image_paths=request.image_paths,
            save_hashes=True
        )
        
        return ImageFraudResponse(
            image_fraud_score=fraud_score,
            duplicate_images=duplicate_count,
            explanation=explanation
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing images: {str(e)}"
        )


@router.get("/image-fraud/status")
async def get_image_fraud_status():
    """Get image fraud detection service status"""
    from app.services.image_fraud import load_image_hashes
    
    hashes = load_image_hashes()
    
    return {
        "status": "operational",
        "service": "Image Fraud Detection",
        "stored_hashes": len(hashes),
        "method": "Perceptual Hashing (pHash)",
        "threshold": "Hamming distance ≤ 8"
    }
