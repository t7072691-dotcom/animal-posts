import os
import sys
import requests
from datetime import datetime
from instagrapi import Client
from dotenv import load_dotenv

load_dotenv()
print(sys.executable)

# --- CONFIG ---
UNSPLASH_KEY = os.getenv("UNSPLASH_ACCESS_KEY")  # Access Key only
INSTAGRAM_USER = os.getenv("IG_USER")
INSTAGRAM_PASS = os.getenv("IG_PASS")
# TIKTOK_TOKEN = os.getenv("TIKTOK_TOKEN")  # optional placeholder

# --- FUNCTIONS ---
def fetch_cute_animal_image():
    """Fetch a random cute animal photo from Unsplash API using your Access Key."""
    url = "https://api.unsplash.com/photos/random"
    params = {"query": "cute animal", "client_id": UNSPLASH_KEY}
    resp = requests.get(url, params=params)
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Unsplash API error:", resp.text)
        raise e
    data = resp.json()
    img_url = data["urls"]["regular"]
    img_data = requests.get(img_url).content
    filename = f"animal_{datetime.now().strftime('%Y%m%d')}.jpg"
    with open(filename, "wb") as f:
        f.write(img_data)
    return filename, img_url
