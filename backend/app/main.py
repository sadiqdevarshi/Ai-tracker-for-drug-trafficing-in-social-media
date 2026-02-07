import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uuid
from datetime import datetime
from pymongo import MongoClient

from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from .models import Post, Alert, RiskScore
from .services import ai_engine

import logging
import asyncio
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Module-level demo samples
DEMO_SAMPLES = [
    {"platform": "Telegram", "content": "Ice and crystal shards available. Discrete shipping.", "author_id": "demo_vendor_1"},
    {"platform": "Instagram", "content": "Got those Xanax bars and Adderall. DM for menu.", "author_id": "demo_vendor_2"},
    {"platform": "Telegram", "content": "Pure white snow just landed. Fast delivery.", "author_id": "demo_vendor_3"},
    {"platform": "Instagram", "content": "New green buds in stock. High quality herb.", "author_id": "demo_vendor_4"},
    {"platform": "Telegram", "content": "Fent patches and bricks available. High purity.", "author_id": "demo_vendor_5"},
    {"platform": "Instagram", "content": "Got those 🍫 and 🍬 for the weekend party. DM for delivery.", "author_id": "demo_vendor_6"},
    {"platform": "Telegram", "content": "Top shelf snow ❄️ available. Pure white. Fast delivery.", "author_id": "demo_vendor_7"},
    {"platform": "Instagram", "content": "Fresh green 🥦 and loud 🔊 vibes only. DM for delivery.", "author_id": "demo_vendor_8"},
    {"platform": "Telegram", "content": "K-pins and footballs in stock. 💊 Blue and yellow bars.", "author_id": "demo_vendor_9"},
    {"platform": "Instagram", "content": "Roxies 30mg. Genuine pharma. Wickr: pharm_plug", "author_id": "demo_vendor_10"}
]

async def demo_mode_loop():
    """Periodically ingests a random sample to keep the dashboard active on Render."""
    logger.info("DEMO MODE: Starting background ingest loop...")
    
    # Wait for app to be fully ready
    await asyncio.sleep(5)
    
    while True:
        try:
            sample = random.choice(DEMO_SAMPLES)
            post_content = f"{sample['content']} [DEMO {datetime.utcnow().strftime('%H:%M:%S')}]"
            
            post = Post(
                platform=sample["platform"],
                content=post_content,
                author_id=sample["author_id"],
                timestamp=datetime.utcnow()
            )
            
            await ingest_post(post)
            logger.info(f"DEMO MODE: Automatically ingested {sample['platform']} signal")
        except Exception as e:
            logger.error(f"DEMO MODE ERROR: Unexpected failure in loop: {e}", exc_info=True)
            
        await asyncio.sleep(30)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    if os.getenv("ENABLE_DEMO_MODE", "true").lower() == "true":
        task = asyncio.create_task(demo_mode_loop())
        logger.info("Lifespan: Demo mode loop task created.")
    yield
    # Shutdown logic (optional)
    if 'task' in locals():
        task.cancel()

app = FastAPI(title="DrugDetect AI API", lifespan=lifespan)

@app.get("/")
async def serve_index():
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        paths_to_check = [
            os.path.join(base_dir, "index.html"),
            "index.html",
            "/opt/render/project/src/index.html"
        ]
        
        for index_path in paths_to_check:
            if os.path.exists(index_path):
                return FileResponse(index_path)
                
        return {"error": "Dashboard index.html not found"}
    except Exception as e:
        return {"error": str(e)}

# Enable CORS
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
    logger.info("Connected to MongoDB")
else:
    db_memory = {"posts": [], "alerts": []}
    posts_col = None
    alerts_col = None
    logger.info("Using in-memory storage (Fallback)")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.utcnow(),
        "storage_mode": "MongoDB" if posts_col is not None else "In-Memory",
        "database_connected": posts_col is not None
    }

@app.get("/debug/memory")
async def debug_memory():
    if posts_col is not None:
        return {"error": "Debugging not available in MongoDB mode"}
    return db_memory

@app.post("/debug/force-ingest")
async def force_ingest():
    sample = random.choice(DEMO_SAMPLES)
    post = Post(
        platform=sample["platform"],
        content=f"{sample['content']} [FORCED {datetime.utcnow().strftime('%H:%M:%S')}]",
        author_id="forced_debug",
        timestamp=datetime.utcnow()
    )
    return await ingest_post(post)

@app.post("/posts/ingest", response_model=Alert)
async def ingest_post(post: Post):
    try:
        # DEDUPLICATION
        if posts_col is not None:
            existing = posts_col.find_one({"content": post.content})
            if existing:
                alert_data = alerts_col.find_one({"post_id": existing["_id"]})
                if alert_data: return Alert(**alert_data)
        else:
            for p in db_memory["posts"]:
                if p.content == post.content:
                    for a in db_memory["alerts"]:
                        if a.post_id == p.id: return a

        # Create Post - Explicitly use 'id' field name
        post_data = post.model_dump(by_alias=True, exclude={"id"})
        new_post = Post(id=str(uuid.uuid4()), **post_data)
        
        if posts_col is not None:
            posts_col.insert_one(new_post.model_dump(by_alias=True))
        else:
            db_memory["posts"].append(new_post)
        
        # Process with AI Engine
        risk = ai_engine.calculate_risk(new_post.content, new_post.image_url)
        
        # Create Alert - Explicitly use 'id' field name
        alert = Alert(
            id=str(uuid.uuid4()),
            post_id=new_post.id,
            risk_score=risk,
            platform=new_post.platform,
            content_preview=new_post.content[:100] + "..." if len(new_post.content) > 100 else new_post.content
        )
        
        if alerts_col is not None:
            alerts_col.insert_one(alert.model_dump(by_alias=True))
        else:
            db_memory["alerts"].append(alert)
            
        return alert
    except Exception as e:
        logger.error(f"INGEST ERROR: Failed to process post: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Track if this worker has done an initial ingest
INITIAL_INGEST_DONE = False

@app.get("/alerts", response_model=List[Alert])
async def get_alerts():
    global INITIAL_INGEST_DONE
    
    # Auto-populate if empty (helpful for multi-worker free tier)
    if not INITIAL_INGEST_DONE and posts_col is None and len(db_memory["posts"]) == 0:
        logger.info("Auto-populating alerts for new worker instance...")
        try:
            await force_ingest()
            INITIAL_INGEST_DONE = True
        except Exception as e:
            logger.error(f"Auto-populate failed: {e}")

    if alerts_col is not None:
        cursor = alerts_col.find().sort("risk_score.score", -1)
        return [Alert(**doc) for doc in cursor]
    return sorted(db_memory["alerts"], key=lambda x: x.risk_score.score, reverse=True)

@app.get("/stats")
async def get_stats():
    # Also trigger auto-populate here just in case
    global INITIAL_INGEST_DONE
    if not INITIAL_INGEST_DONE and posts_col is None and len(db_memory["posts"]) == 0:
        try:
            await force_ingest()
            INITIAL_INGEST_DONE = True
        except: pass

    if posts_col is not None:
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
        "platform_distribution": {"Telegram": telegram, "Instagram": instagram}
    }
