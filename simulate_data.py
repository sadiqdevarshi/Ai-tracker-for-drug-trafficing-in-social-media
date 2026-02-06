import requests
import time
import random

API_URL = "http://localhost:8000/posts/ingest"

SAMPLES = [
    # HIGH RISK - Multiple drug keywords + delivery terms
    {
        "platform": "Telegram",
        "content": "New stock of ICE available. High quality crystal. Delivery anywhere in the city. DM for prices.",
        "author_id": "user_123",
        "image_url": "http://example.com/suspicious_pills.jpg"
    },
    {
        "platform": "Telegram",
        "content": "Premium meth crystal in stock. Discrete shipping worldwide. Telegram me for samples. Fast delivery guaranteed.",
        "author_id": "user_dealer_01",
        "image_url": "http://example.com/drug_package.jpg"
    },
    {
        "platform": "Instagram",
        "content": "Got the best ice and pills in town 💎 Delivery 24/7. DM for wickr contact. Discrete packaging guaranteed.",
        "author_id": "supplier_99",
        "image_url": "http://example.com/suspicious_pills.jpg"
    },
    {
        "platform": "Telegram",
        "content": "Crystal meth available now. High purity. Shipping to all locations. Contact my plug for stash details.",
        "author_id": "vendor_xyz",
        "image_url": "http://example.com/drug_stash.jpg"
    },
    
    # MEDIUM RISK - Some suspicious keywords but less obvious
    {
        "platform": "Telegram",
        "content": "Looking for a plug for some discrete shipping. Need pills ASAP.",
        "author_id": "user_789"
    },
    {
        "platform": "Instagram",
        "content": "Anyone know where to get good stuff? Need delivery service. DM me if you can help.",
        "author_id": "seeker_123"
    },
    {
        "platform": "Telegram",
        "content": "Need a reliable plug in the area. Looking for discrete transactions. Hit me up on wickr.",
        "author_id": "buyer_456"
    },
    {
        "platform": "Instagram",
        "content": "Selling special party supplies 🎉 Fast shipping available. Telegram for details.",
        "author_id": "party_vendor"
    },
    {
        "platform": "Telegram",
        "content": "Got what you need. Discrete and fast. Message me for the stash location.",
        "author_id": "connect_789"
    },
    
    # LOW RISK - Normal social media content
    {
        "platform": "Instagram",
        "content": "Just hanging out at the beach! #summer #vibes",
        "author_id": "user_456",
        "image_url": "http://example.com/beach.jpg"
    },
    {
        "platform": "Instagram",
        "content": "Check out these new vitamin supplements I found! #health #vitamins",
        "author_id": "user_000",
        "image_url": "http://example.com/vitamins.jpg"
    },
    {
        "platform": "Instagram",
        "content": "Beautiful sunset today 🌅 Feeling grateful! #nature #photography",
        "author_id": "photographer_01"
    },
    {
        "platform": "Telegram",
        "content": "Anyone want to join our study group? We meet every Tuesday at the library.",
        "author_id": "student_group"
    },
    {
        "platform": "Instagram",
        "content": "New recipe alert! 🍕 Homemade pizza night with the family. #cooking #foodie",
        "author_id": "chef_mom",
        "image_url": "http://example.com/pizza.jpg"
    },
    {
        "platform": "Telegram",
        "content": "Selling my old laptop. Great condition, barely used. DM for price.",
        "author_id": "tech_seller"
    },
    {
        "platform": "Instagram",
        "content": "Morning workout done! 💪 Feeling energized. #fitness #motivation",
        "author_id": "gym_enthusiast"
    },
    
    # MEDIUM-HIGH RISK - Coded language
    {
        "platform": "Telegram",
        "content": "Fresh batch just arrived. Top quality product. Delivery available. Contact for samples.",
        "author_id": "supplier_coded"
    },
    {
        "platform": "Instagram",
        "content": "Special items in stock 💎 Fast shipping. Serious inquiries only. Telegram in bio.",
        "author_id": "vendor_coded"
    },
    
    # HIGH RISK - Direct drug references
    {
        "platform": "Telegram",
        "content": "Pure crystal available. Best prices in the city. Discrete delivery to your door. DM now.",
        "author_id": "dealer_direct",
        "image_url": "http://example.com/pill_bottle.jpg"
    },
    {
        "platform": "Instagram",
        "content": "Pills pills pills 💊 All types available. Shipping worldwide. Wickr: dealer420",
        "author_id": "pill_vendor",
        "image_url": "http://example.com/suspicious_pills.jpg"
    },
    
    # LOW RISK - Business/Commerce
    {
        "platform": "Instagram",
        "content": "New clothing collection dropping tomorrow! 👕 Free shipping on orders over $50. #fashion #sale",
        "author_id": "clothing_store"
    },
    {
        "platform": "Telegram",
        "content": "Selling handmade jewelry. Custom orders welcome. Shipping available worldwide. Check my portfolio!",
        "author_id": "jewelry_maker"
    },
    {
        "platform": "Instagram",
        "content": "Fresh organic vegetables from our farm 🥕🥬 Delivery available in the city. #organic #farmfresh",
        "author_id": "local_farmer"
    },
    
    # MEDIUM RISK - Ambiguous content
    {
        "platform": "Telegram",
        "content": "Got the good stuff. Hit me up for details. Fast and discrete.",
        "author_id": "ambiguous_01"
    },
    {
        "platform": "Instagram",
        "content": "Premium quality guaranteed. Delivery service available. DM for menu.",
        "author_id": "ambiguous_02"
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
