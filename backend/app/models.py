from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class RiskScore(BaseModel):
    score: int = Field(..., ge=0, le=100)
    level: str  # Low, Medium, High
    nlp_confidence: float
    image_confidence: float
    behavioral_score: float
    reasoning: List[str]

class Post(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    platform: str  # "Telegram" or "Instagram"
    content: str
    image_url: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    author_id: str
    is_processed: bool = False

class Alert(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    post_id: str
    risk_score: RiskScore
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = "Pending"  # Pending, Flagged, Dismissed
    platform: str
    content_preview: str
