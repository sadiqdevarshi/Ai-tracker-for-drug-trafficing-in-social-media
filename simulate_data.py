import os
import requests
import time
import random

# Allow overriding the API URL via environment variable for Render deployment
API_URL = os.getenv("API_URL", "http://localhost:8000/posts/ingest")

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
    },

    # NEW: UK Slang / Regional
    {
        "platform": "Telegram",
        "content": "Peng gear ❄️ just landed. Banging white. 10/10 quality. Hit me up for the drop off 🚗💨 London based.",
        "author_id": "ldn_plugs"
    },
    {
        "platform": "Instagram",
        "content": "Got those cali tins 🍧 and packs 📦 available. Top shelf flavors only. DM for the menu link.",
        "author_id": "cali_import_uk"
    },

    # NEW: Coded Emojis / Gen Z Slang
    {
        "platform": "Instagram",
        "content": "Anyone need some 🍭 or 🍬 for the rave tonight? 🕺 Active all night. Fast delivery. 🚀",
        "author_id": "party_essentials_00"
    },
    {
        "platform": "Telegram",
        "content": "Need a reliable 🔌 for the 🍄? Taking orders now for the weekend trip. 🌈🚀",
        "author_id": "trippy_vibes"
    },

    # NEW: Crypto-linked transactions
    {
        "platform": "Telegram",
        "content": "All meds available. Accepting BTC/XMR for discrete transactions. 🔐 Verified vendor with 500+ reviews. DM for shop link.",
        "author_id": "dark_market_vendor"
    },

    # NEW: Professional/Educational (Noise level)
    {
        "platform": "Instagram",
        "content": "New research published on the effects of crystals in industrial engineering! 🔬🏗️ #science #engineering",
        "author_id": "science_daily"
    },
    {
        "platform": "Telegram",
        "content": "Weekly pharmacy stock update: All standard medications and vitamins are back in inventory. Please visit your local clinic.",
        "author_id": "health_ministry_official"
    },

    # NEW: More diverse pharmaceutical samples
    {
        "platform": "Telegram",
        "content": "Valium / Diazepam / Klonopin in stock. 💊 Sealed blisters. Direct from factory. Worldwide discrete shipping.",
        "author_id": "benzo_supply_chain"
    },
    {
        "platform": "Instagram",
        "content": "Codeine syrup 🍼 and prometh 🍇 in stock. Genuine sealed bottles. DM for prices while stock lasts.",
        "author_id": "syrup_central"
    },

    # NEW: Normal social activity variations
    {
        "platform": "Instagram",
        "content": "Walking through the green fields of Switzerland today. 🇨🇭 Peaceful and beautiful. #travel #nature",
        "author_id": "globetrotter_jane"
    },
    {
        "platform": "Telegram",
        "content": "Selling my collection of vintage stamps. 📮 Collection date from 1920-1950. DM for catalog.",
        "author_id": "stamp_collector_king"
    },

    # NEW: Suspicious but cleverly worded
    {
        "platform": "Instagram",
        "content": "If you know, you know. 🤐 Everything you need for the perfect night. DM is open 24/7. #nightlife #vibes",
        "author_id": "iykyk_anonymous"
    },
    {
        "platform": "Telegram",
        "content": "Moving locations. Clearing all old stash. Everything must go today. Cheap deals if you buy in weight. DM current location.",
        "author_id": "clearance_sale_plugs"
    },

    # NEW: Regional Slang (US South)
    {
        "platform": "Instagram",
        "content": "I got the best herb 🌿 in the dirty south. Big buds, no seeds. Pull up or hit my line for the drop.",
        "author_id": "atl_herbalist"
    },

    # NEW: Normal Commerce
    {
        "platform": "Instagram",
        "content": "New shipment of high-end white t-shirts just arrived! 👕 Minimalist design, pure cotton. Shop link in bio.",
        "author_id": "minimalist_fashion"
    }
]

def simulate():
    print(f"Starting infinite simulation... Target: {API_URL}")
    print("Each cycle will shuffle the 40+ unique samples.")
    
    cycle_count = 1
    while True:
        print(f"\n--- Starting Cycle {cycle_count} ---")
        shuffled_samples = list(SAMPLES)
        random.shuffle(shuffled_samples)
        
        for sample in shuffled_samples:
            # FORCE UNIQUENESS: Add a timestamp to the content 
            # so every single signal is unique even if the base text is shared.
            unique_sample = dict(sample)
            timestamp = time.strftime("%H:%M:%S")
            unique_sample["content"] = f"{sample['content']} [ID: {timestamp}-{random.randint(100,999)}]"
            
            try:
                resp = requests.post(API_URL, json=unique_sample)
                if resp.status_code == 200:
                    alert = resp.json()
                    print(f"[{unique_sample['platform']}] Ingested Unique: {unique_sample['content'][:40]}...")
                else:
                    print(f"Backend returned: {resp.status_code}")
            except Exception as e:
                print(f"Connection Error: {e}")
            
            time.sleep(4) # Balanced speed for monitoring
            
        cycle_count += 1
        print(f"\n--- Cycle complete. Shuffling for next run... ---")

if __name__ == "__main__":
    simulate()
