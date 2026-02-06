import requests
import time
import random

API_URL = "http://localhost:8000/posts/ingest"

SAMPLES = [
    # HIGH RISK - Pharmaceutical diverstion
    {
        "platform": "Instagram",
        "content": "Xanax bars and Adderall 30mg available. Genuine pharmaceutical grade. Overnight shipping 📦 DM for menu and wickr.",
        "author_id": "pharma_connect",
        "image_url": "http://example.com/pharmacy_bottles.png"
    },
    {
        "platform": "Telegram",
        "content": "OxyContin 80mg / Percocet in stock now. Bulk deals available. Discrete delivery worldwide 🌍 Telegram @med_plug",
        "author_id": "pill_supplier_pro"
    },

    # HIGH RISK - Street Slang 
    {
        "platform": "Telegram",
        "content": "Top shelf snow ❄️ available. Pure white. Fast delivery within the city. Hit up the plug for stash location.",
        "author_id": "snow_man_88"
    },
    {
        "platform": "Instagram",
        "content": "Fresh green 🥦 and loud 🔊 vibes only. High quality bud. DM for delivery options. Serious buyers only.",
        "author_id": "vibes_daily"
    },

    # MEDIUM RISK - Suspicious commerce
    {
        "platform": "Telegram",
        "content": "Need someone who can handle unmarked shipping. Looking for a long term partner for wholesale. DM now.",
        "author_id": "biz_dev_dark"
    },
    {
        "platform": "Instagram",
        "content": "Special private deal today only 💎 Everything must go. Fast shipping anywhere. Check bio link for contact.",
        "author_id": "exclusive_deals_01"
    },

    # LOW RISK - Educational/Medical (False positive testing)
    {
        "platform": "Instagram",
        "content": "Pharmacy students studying for exams today! Hard work pays off 📚 #medical #studentlife",
        "author_id": "med_student_01",
        "image_url": "http://example.com/books.jpg"
    },
    {
        "platform": "Telegram",
        "content": "Please remember to take your prescribed vitamins daily. Health is wealth! Join our wellness channel.",
        "author_id": "health_facts"
    },

    # LOW RISK - Regular Commerce
    {
        "platform": "Instagram",
        "content": "Selling my collection of rare crystal stones 💎 DM for prices. Each piece is unique! #crystals #healing",
        "author_id": "crystal_seller"
    },
    {
        "platform": "Telegram",
        "content": "Flash sale on all laptops! Shipping included in the price. Check the list of specs below.",
        "author_id": "tech_hub"
    },

    # HIGH RISK - Fentanyl references
    {
        "platform": "Telegram",
        "content": "Fent patches and bricks available. High purity. Local pickup or discrete shipping. Safe transactions only.",
        "author_id": "supplier_bulk"
    },

    # MEDIUM RISK - Coded language with emojis
    {
        "platform": "Instagram",
        "content": "Got those 🍫 and 🍬 for the weekend party. DM for delivery. Limited stock left!",
        "author_id": "party_host_00"
    },

    # LOW RISK - Nature/Art
    {
        "platform": "Instagram",
        "content": "The snow on the mountains looks beautiful today! 🏔️ Wishing I was there. #winter #nature",
        "author_id": "nature_lover"
    },
    {
        "platform": "Instagram",
        "content": "New green art piece finished! 🎨 What do you think of the color palette? #artist #painting",
        "author_id": "art_studio"
    },

    # HIGH RISK - Direct weight references
    {
        "platform": "Telegram",
        "content": "Selling by the oz or gram. Best quality meth stash. Direct message to get the location. No time wasters.",
        "author_id": "bulk_dealer_pro"
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
