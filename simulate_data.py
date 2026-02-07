import os
import requests
import time
import random
from datetime import datetime

# Allow overriding the API URL via environment variable for Render deployment
API_URL = os.getenv("API_URL", "http://localhost:8000/posts/ingest")

# TEMPLATE DATA for generating unique sentences
DRUGS = [
    "Xanax", "Adderall", "Oxy", "Percocet", "Ice", "Crystal", "Meth", 
    "Snow", "White girl", "Buds", "Green", "Herb", "Coke", "Lean", 
    "Dirty sprite", "M30 blues", "K-pins", "Football", "Tina", "Glass"
]

ADJECTIVES = [
    "Pure", "High quality", "Top shelf", "Sealed", "Pharma grade", 
    "Banging", "10/10", "Fresh", "Uncut", "Genuine", "Powerful"
]

DELIVERY = [
    "Discrete shipping", "Overnight delivery", "Direct drop", "Fast shipping", 
    "Local pickup", "Worldwide delivery", "Unmarked packaging", "Safe drop"
]

PLATFORMS = ["Telegram", "Instagram"]

CONNECTS = [
    "DM for menu", "Hit the wickr", "Telegram me", "Check bio link", 
    "Signal for details", "Private message me"
]

EMOJIS = ["📦", "💊", "❄️", "🔌", "🥦", "🍇", "💎", "🚀", "🤫"]

def generate_sentence():
    """Generates a unique, natural-sounding drug trafficking signal."""
    # Logic for different types of sentences
    r = random.random()
    
    if r < 0.3: # "Direct sale" type
        return f"{random.choice(ADJECTIVES)} {random.choice(DRUGS)} available now. {random.choice(DELIVERY)}. {random.choice(CONNECTS)} {random.choice(EMOJIS)}"
    elif r < 0.6: # "New drop" type
        return f"New {random.choice(DRUGS)} drop just landed! {random.choice(ADJECTIVES)} quality. {random.choice(CONNECTS)} for {random.choice(DELIVERY)}. {random.choice(EMOJIS)}"
    elif r < 0.8: # "Short & Urgent" type
        return f"Got {random.choice(DRUGS)}. {random.choice(DELIVERY)} only. {random.choice(CONNECTS)} {random.choice(EMOJIS)}"
    else: # "Regional/Slang" type
        return f"Best {random.choice(DRUGS)} in town. {random.choice(ADJECTIVES)} vibes. {random.choice(CONNECTS)}. {random.choice(EMOJIS)}"

def simulate():
    print(f"🚀 Starting DYNAMIC simulation...")
    print(f"Target: {API_URL}")
    print("Generating unique sentences using template engine...")
    
    count = 1
    while True:
        try:
            platform = random.choice(PLATFORMS)
            content = generate_sentence()
            author_id = f"user_{random.randint(1000, 9999)}"
            
            # Add a micro-timestamp for absolute uniqueness in deduplication
            final_content = f"{content} [{datetime.now().strftime('%H:%M:%S')}]"
            
            payload = {
                "platform": platform,
                "content": final_content,
                "author_id": author_id
            }
            
            resp = requests.post(API_URL, json=payload, timeout=5)
            if resp.status_code == 200:
                print(f"[{count}] Sent: {final_content[:60]}...")
            else:
                print(f"[{count}] Failed: {resp.status_code}")
                
        except Exception as e:
            print(f"[{count}] Error: {e}")
            
        count += 1
        time.sleep(random.uniform(5, 10)) # Random delay for natural frequency

if __name__ == "__main__":
    simulate()
