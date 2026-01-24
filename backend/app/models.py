from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from .database import Base
import datetime

class ListingHistory(Base):
    __tablename__ = "listing_history"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    area_sqft = Column(Float)
    city = Column(String)
    locality = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Analysis results
    fraud_probability = Column(Float)
    fraud_types = Column(JSON)  # Stores list of fraud types
    explanations = Column(JSON)  # Stores list of explanations
    module_scores = Column(JSON)  # Stores dict of module scores
    
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
