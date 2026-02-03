from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uuid
from datetime import datetime

from .models import Post, Alert, RiskScore
from .services import ai_engine

app = FastAPI(title="DrugDetect AI API")

# Enable CORS for React development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo purposes
db = {
    "posts": [],
    "alerts": []
}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.post("/posts/ingest", response_model=Alert)
async def ingest_post(post: Post):
    post.id = str(uuid.uuid4())
    db["posts"].append(post)
    
    # Process with AI Engine
    risk = ai_engine.calculate_risk(post.content, post.image_url)
    
    # Create Alert
    alert = Alert(
        id=str(uuid.uuid4()),
        post_id=post.id,
        risk_score=risk,
        platform=post.platform,
        content_preview=post.content[:100] + "..." if len(post.content) > 100 else post.content
    )
    
    db["alerts"].append(alert)
    return alert

@app.get("/alerts", response_model=List[Alert])
async def get_alerts():
    return sorted(db["alerts"], key=lambda x: x.risk_score.score, reverse=True)

@app.get("/stats")
async def get_stats():
    return {
        "total_processed": len(db["posts"]),
        "high_risk_alerts": len([a for a in db["alerts"] if a.risk_score.level == "High"]),
        "platform_distribution": {
            "Telegram": len([p for p in db["posts"] if p.platform == "Telegram"]),
            "Instagram": len([p for p in db["posts"] if p.platform == "Instagram"])
        }
    }
