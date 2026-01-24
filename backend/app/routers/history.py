from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import ListingHistory
from .analyze import ListingData, FraudReport
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class HistoryCreate(BaseModel):
    listing_data: ListingData
    analysis_results: FraudReport

class HistoryResponse(BaseModel):
    id: int
    title: str
    city: str
    locality: str
    price: float
    fraud_probability: float
    fraud_types: List[str]
    timestamp: datetime

    class Config:
        from_attributes = True

class HistoryDetailResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    area_sqft: float
    city: str
    locality: str
    latitude: float
    longitude: float
    fraud_probability: float
    fraud_types: List[str]
    explanations: List[str]
    module_scores: dict
    timestamp: datetime

    class Config:
        from_attributes = True

@router.post("/history", response_model=HistoryResponse)
async def save_history(data: HistoryCreate, db: Session = Depends(get_db)):
    """
    Save an analyzed listing to the database.
    """
    db_history = ListingHistory(
        title=data.listing_data.title,
        description=data.listing_data.description,
        price=data.listing_data.price,
        area_sqft=data.listing_data.area_sqft,
        city=data.listing_data.city,
        locality=data.listing_data.locality,
        latitude=data.listing_data.latitude,
        longitude=data.listing_data.longitude,
        fraud_probability=data.analysis_results.fraud_probability,
        fraud_types=data.analysis_results.fraud_types,
        explanations=data.analysis_results.explanations,
        module_scores=data.analysis_results.module_scores
    )
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

@router.get("/history", response_model=List[HistoryResponse])
async def get_history(db: Session = Depends(get_db)):
    """
    Fetch all analysis history.
    """
    return db.query(ListingHistory).order_by(ListingHistory.timestamp.desc()).all()

@router.get("/history/{history_id}", response_model=HistoryDetailResponse)
async def get_history_detail(history_id: int, db: Session = Depends(get_db)):
    """
    Fetch detailed analysis history for a specific ID.
    """
    history = db.query(ListingHistory).filter(ListingHistory.id == history_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="History not found")
    return history
