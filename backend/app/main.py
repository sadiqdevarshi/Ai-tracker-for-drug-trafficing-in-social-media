import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uuid
from datetime import datetime
from pymongo import MongoClient

from .models import Post, Alert, RiskScore
from .services import ai_engine

app = FastAPI(title="DrugDetect AI API")

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
if MONGODB_URI:
    client = MongoClient(MONGODB_URI)
    db_conn = client.get_database("drugdetect_db")
    posts_col = db_conn.posts
    alerts_col = db_conn.alerts
    print("Connected to MongoDB")
else:
    # In-memory storage fallback for local development
    db_memory = {
        "posts": [],
        "alerts": []
    }
    posts_col = None
    alerts_col = None
    print("Using in-memory storage (Fallback)")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.post("/posts/ingest", response_model=Alert)
async def ingest_post(post: Post):
    post.id = str(uuid.uuid4())
    
    if posts_col is not None:
        posts_col.insert_one(post.dict(by_alias=True))
    else:
        db_memory["posts"].append(post)
    
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
    
    if alerts_col is not None:
        alerts_col.insert_one(alert.dict(by_alias=True))
    else:
        db_memory["alerts"].append(alert)
        
    return alert

@app.get("/alerts", response_model=List[Alert])
async def get_alerts():
    if alerts_col is not None:
        alerts = list(alerts_col.find().sort("risk_score.score", -1))
        # Convert _id to id if necessary (handled by Pydantic usually)
        return alerts
    return sorted(db_memory["alerts"], key=lambda x: x.risk_score.score, reverse=True)

@app.post("/reset")
async def reset_data():
    if posts_col is not None and alerts_col is not None:
        posts_col.delete_many({})
        alerts_col.delete_many({})
    else:
        db_memory["posts"] = []
        db_memory["alerts"] = []
    return {"message": "All tracking data has been reset to zero."}

@app.get("/stats")
async def get_stats():
    if posts_col is not None and alerts_col is not None:
        total = posts_col.count_documents({})
        high_risk = alerts_col.count_documents({"risk_score.level": "High"})
        telegram = posts_col.count_documents({"platform": "Telegram"})
        instagram = posts_col.count_documents({"platform": "Instagram"})
    else:
        total = len(db_memory["posts"])
        high_risk = len([a for a in db_memory["alerts"] if a.risk_score.level == "High"])
        telegram = len([p for p in db_memory["posts"] if p.platform == "Telegram"])
        instagram = len([p for p in db_memory["posts"] if p.platform == "Instagram"])

    return {
        "total_processed": total,
        "high_risk_alerts": high_risk,
        "platform_distribution": {
            "Telegram": telegram,
            "Instagram": instagram
        }
    }
