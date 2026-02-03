import requests
import time
import random

API_URL = "http://localhost:8000/posts/ingest"

SAMPLES = [
    {
        "platform": "Telegram",
        "content": "New stock of ICE available. High quality crystal. Delivery anywhere in the city. DM for prices.",
        "author_id": "user_123",
        "image_url": "http://example.com/suspicious_pills.jpg"
    },
    {
        "platform": "Instagram",
        "content": "Just hanging out at the beach! #summer #vibes",
        "author_id": "user_456",
        "image_url": "http://example.com/beach.jpg"
    },
    {
        "platform": "Telegram",
        "content": "Looking for a plug for some discrete shipping. Need pills ASAP.",
        "author_id": "user_789"
    },
    {
        "platform": "Instagram",
        "content": "Check out these new vitamin supplements I found! #health #vitamins",
        "author_id": "user_000",
        "image_url": "http://example.com/vitamins.jpg"
    }
]

def simulate():
    print("Starting simulation... (Ensure backend is running at http://localhost:8000)")
    while True:
        sample = random.choice(SAMPLES)
        try:
            resp = requests.post(API_URL, json=sample)
            if resp.status_code == 200:
                alert = resp.json()
                print(f"Ingested: {sample['platform']} - Risk: {alert['risk_score']['score']}% ({alert['risk_score']['level']})")
        except Exception as e:
            print(f"Error connecting to backend: {e}")
        
        time.sleep(5)

if __name__ == "__main__":
    simulate()
