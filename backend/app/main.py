import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uuid
from datetime import datetime
from pymongo import MongoClient

from fastapi.responses import FileResponse
from .models import Post, Alert, RiskScore
from .services import ai_engine

import logging

# Configure logging to see errors in Render logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="DrugDetect AI API")

@app.get("/")
async def serve_index():
    try:
        # Try multiple potential paths for index.html
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        paths_to_check = [
            os.path.join(base_dir, "index.html"),
            "index.html",
            "/opt/render/project/src/index.html"
        ]
        
        for index_path in paths_to_check:
            if os.path.exists(index_path):
                logger.info(f"Serving index from: {index_path}")
                return FileResponse(index_path)
                
        logger.error("index.html not found in any expected location")
        return {"error": "Dashboard index.html not found", "checked_paths": paths_to_check}
    except Exception as e:
        logger.error(f"Error serving index: {e}")
        return {"error": str(e)}

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
    storage = "MongoDB" if posts_col is not None else "In-Memory (Fallback)"
    return {
        "status": "healthy", 
        "timestamp": datetime.utcnow(),
        "storage_mode": storage,
        "database_connected": posts_col is not None
    }

@app.post("/posts/ingest", response_model=Alert)
async def ingest_post(post: Post):
    # DEDUPLICATION: Check if this content was already processed
    if posts_col is not None:
        existing = posts_col.find_one({"content": post.content})
        if existing:
            # Return the existing alert if we've already seen this content
            # PyMongo dicts use "_id"
            alert_data = alerts_col.find_one({"post_id": existing["_id"]})
            if alert_data:
                return alert_data
            # If post exists but alert doesn't, we continue to create it
    else:
        # Memory fallback check
        for p in db_memory["posts"]:
            if p.content == post.content:
                for a in db_memory["alerts"]:
                    if a.post_id == p.id:
                        return a

    # Create Post with explicit _id for Pydantic alias mapping
    post_data = post.dict(exclude={"id"})
    new_post = Post(_id=str(uuid.uuid4()), **post_data)
    
    if posts_col is not None:
        # Insert using dict with _id
        posts_col.insert_one(new_post.dict(by_alias=True))
        logger.info(f"Ingested post to MongoDB: {new_post.id}")
    else:
        db_memory["posts"].append(new_post)
        logger.info(f"Ingested post to Memory: {new_post.id}")
    
    # Process with AI Engine
    risk = ai_engine.calculate_risk(new_post.content, new_post.image_url)
    
    # Create Alert with explicit _id
    alert = Alert(
        _id=str(uuid.uuid4()),
        post_id=new_post.id,
        risk_score=risk,
        platform=new_post.platform,
        content_preview=new_post.content[:100] + "..." if len(new_post.content) > 100 else new_post.content
    )
    
    if alerts_col is not None:
        alerts_col.insert_one(alert.dict(by_alias=True))
        logger.info(f"Created alert in MongoDB: {alert.id}")
    else:
        db_memory["alerts"].append(alert)
        logger.info(f"Created alert in Memory: {alert.id}")
        
    return alert

@app.get("/alerts", response_model=List[Alert])
async def get_alerts():
    if alerts_col is not None:
        # Fetch high-risk alerts first
        cursor = alerts_col.find().sort("risk_score.score", -1)
        alerts = []
        for doc in cursor:
            # Pydantic will map _id to id if populate_by_name is True
            alerts.append(Alert(**doc))
        return alerts
    return sorted(db_memory["alerts"], key=lambda x: x.risk_score.score, reverse=True)


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
