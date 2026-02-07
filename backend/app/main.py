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

# Signal Generation Templates
VARIETY_DATA = {
    "drugs": ["Xanax", "Adderall", "Oxy", "Percocet", "Ice", "Crystal", "Meth", "Snow", "Buds", "Green", "Lean", "M30 blues", "K-pins", "Football", "Tina", "Glass"],
    "adjectives": ["Pure", "High quality", "Top shelf", "Sealed", "Pharma grade", "Banging", "10/10", "Fresh", "Uncut", "Genuine"],
    "delivery": ["Discrete shipping", "Overnight delivery", "Direct drop", "Fast shipping", "Local pickup", "Worldwide delivery", "Unmarked packaging", "Safe drop"],
    "connects": ["DM for menu", "Hit the wickr", "Telegram me", "Check bio link", "Signal for details", "Private message me"],
    "emojis": ["📦", "💊", "❄️", "🔌", "🥦", "🍇", "💎", "🚀", "🤫"]
}

def generate_demo_content():
    r = random.random()
    d = VARIETY_DATA
    drug = random.choice(d["drugs"])
    adj = random.choice(d["adjectives"])
    delivery = random.choice(d["delivery"])
    conn = random.choice(d["connects"])
    emoji = random.choice(d["emojis"])
    
    if r < 0.3:
        return f"{adj} {drug} available now. {delivery}. {conn} {emoji}"
    elif r < 0.6:
        return f"New {drug} drop just landed! {adj} quality. {conn} for {delivery}. {emoji}"
    elif r < 0.8:
        return f"Got {drug}. {delivery} only. {conn} {emoji}"
    else:
        return f"Best {drug} in town. {adj} vibes. {conn}. {emoji}"

async def demo_mode_loop():
    """Periodically generates and ingests unique signals to keep the dashboard active."""
    logger.info("DEMO MODE: Starting background dynamic ingest loop...")
    await asyncio.sleep(5)
    
    while True:
        try:
            platform = random.choice(["Telegram", "Instagram"])
            content = generate_demo_content()
            # Absolute uniqueness for deduplication
            post_content = f"{content} [DEMO {datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]}]"
            
            post = Post(
                platform=platform,
                content=post_content,
                author_id=f"demo_v2_{random.randint(100, 999)}",
                timestamp=datetime.utcnow()
            )
            
            await ingest_post(post)
            logger.info(f"DEMO MODE: Automatically generated {platform} variety signal")
        except Exception as e:
            logger.error(f"DEMO MODE ERROR: {e}", exc_info=True)
            
        await asyncio.sleep(random.uniform(5, 15)) # Faster, more realistic demo flow

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
        # Log CWD to debug Render file environment
        cwd = os.getcwd()
        logger.info(f"Serving request. CWD: {cwd}")
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        paths_to_check = [
            os.path.join(base_dir, "index.html"),
            os.path.join(cwd, "index.html"),
            os.path.join(cwd, "backend", "index.html"), # Just in case
            "index.html",
            "/opt/render/project/src/index.html"
        ]
        
        for index_path in paths_to_check:
            if os.path.exists(index_path):
                logger.info(f"Found index.html at: {index_path}")
                return FileResponse(index_path)
        
        logger.error(f"index.html NOT FOUND. Checked: {paths_to_check}")
        return {"error": "Dashboard index.html not found", "checked_paths": paths_to_check, "cwd": cwd}
    except Exception as e:
        logger.error(f"Error serving index: {e}")
        return {"error": str(e)}

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def ping():
    return {"status": "ok", "message": "Backend is reachable", "version": "v1.2.4-variety", "timestamp": datetime.utcnow()}

# Database Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
logger.info(f"Checking MONGODB_URI environment variable... {'Set' if MONGODB_URI else 'Not Set'}")
if MONGODB_URI:
    try:
        # Added 5s timeout to prevent startup hang if DB is unreachable
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        # Trigger a quick check
        client.admin.command('ping')
        db_conn = client.get_database("drugdetect_db")
        posts_col = db_conn.posts
        alerts_col = db_conn.alerts
        logger.info("Successfully connected to MongoDB")
    except Exception as e:
        logger.error(f"MongoDB Connection Failed: {e}")
        posts_col = None
        alerts_col = None
else:
    db_memory = {"posts": [], "alerts": []}
    posts_col = None
    alerts_col = None
    logger.warning("!!! RUNNING IN IN-MEMORY STORAGE MODE !!!")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.utcnow(),
        "storage_mode": "Persistent (MongoDB)" if posts_col is not None else "In-Memory (Ephemeral)",
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
