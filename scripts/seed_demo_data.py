import requests
import time
import os
import random

WEBHOOK_URL = "http://localhost:8000/webhook/leads"

MOCK_LEADS = [
    {"email": "contact@stripe.com", "name": "Patrick Collison", "source": "organic"},
    {"email": "info@openai.com", "name": "Sam Altman", "source": "referral"},
    {"email": "sales@hubspot.com", "name": "Brian Halligan", "source": "paid_ads"},
    {"email": "hello@vercel.com", "name": "Guillermo Rauch", "source": "organic"},
    {"email": "founder@localbakerynyc.com", "name": "John Dough", "source": "maps"},
    {"email": "marketing@nike.com", "name": "John Donahoe", "source": "referral"},
    {"email": "dev@dbtlabs.com", "name": "Tristan Handy", "source": "organic"},
    {"email": "contact@midjourney.com", "name": "David Holz", "source": "organic"},
    {"email": "support@salesforce.com", "name": "Marc Benioff", "source": "organic"},
    {"email": "admin@bobsplumbing.com", "name": "Bob Smith", "source": "maps"},
    {"email": "ceo@anthropic.com", "name": "Dario Amodei", "source": "referral"},
    {"email": "info@clearbit.com", "name": "Alex MacCaw", "source": "organic"},
    {"email": "contact@framer.com", "name": "Koen Bok", "source": "paid_ads"},
    {"email": "hello@linear.app", "name": "Karri Saarinen", "source": "organic"},
    {"email": "support@superhuman.com", "name": "Rahul Vohra", "source": "referral"},
    {"email": "owner@miamidesigners.co", "name": "Sarah Jenkins", "source": "organic"},
    {"email": "founder@indiehackers.com", "name": "Courtland Allen", "source": "referral"},
    {"email": "contact@apple.com", "name": "Tim Cook", "source": "organic"},
    {"email": "ceo@zoom.us", "name": "Eric Yuan", "source": "paid_ads"},
    {"email": "hello@airbnb.com", "name": "Brian Chesky", "source": "organic"}
]

def seed_data():
    print("[Seeder] Starting to seed Mock Demo Data...")
    
    # Optional: wait for FastAPI to fully spin up
    time.sleep(5)
    
    success_count = 0
    for lead in MOCK_LEADS:
        try:
            res = requests.post(WEBHOOK_URL, json=lead)
            if res.status_code == 200:
                print(f"[Seeder] -> Ingested {lead['email']}")
                success_count += 1
            else:
                print(f"[Seeder] -> Failed {lead['email']}: {res.status_code}")
        except Exception as e:
            print(f"[Seeder] -> Connection Error for {lead['email']}: {e}")
            
        # Add slight delay so output is readable and waterfall has time to catch up
        time.sleep(1)
        
    print(f"[Seeder] Completed! Seeded {success_count}/{len(MOCK_LEADS)} mock leads.")

if __name__ == "__main__":
    if os.getenv("TEST_MODE", "false").lower() == "true":
        seed_data()
    else:
        print("[Seeder] TEST_MODE is not true. Skipping seeding.")
