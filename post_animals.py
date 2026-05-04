import os
import requests
from datetime import datetime
from instagrapi import Client
from dotenv import load_dotenv
load_dotenv()

import sys
print(sys.executable)

# --- CONFIG ---
UNSPLASH_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
INSTAGRAM_USER = os.getenv("IG_USER")
INSTAGRAM_PASS = os.getenv("IG_PASS")
#TIKTOK_TOKEN = os.getenv("TIKTOK_TOKEN")  # optional placeholder


# --- FUNCTIONS ---
def fetch_cute_animal_image():
    """Fetch a random cute animal photo from Unsplash API using your secret key."""
    url = "https://api.unsplash.com/photos/random"
    params = {"query": "cute animal", "client_id": UNSPLASH_KEY}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    img_url = data["urls"]["regular"]
    img_data = requests.get(img_url).content
    filename = f"animal_{datetime.now().strftime('%Y%m%d')}.jpg"
    with open(filename, "wb") as f:
        f.write(img_data)
    return filename, img_url

def post_instagram(image_path, caption="Daily dose of cuteness 🐾"):
    """Login with secrets and post to Instagram."""
    cl = Client()
    cl.login(INSTAGRAM_USER, INSTAGRAM_PASS)
    cl.photo_upload(image_path, caption)

def post_tiktok(image_path, caption="Daily dose of cuteness 🐾"):
    """Placeholder for TikTok posting."""
    print(f"[DEBUG] Would post {image_path} to TikTok with caption: {caption}")

def log_activity(image_url):
    """Save a log file with the image URL and timestamp."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.txt")
    with open(log_file, "w") as f:
        f.write(f"Posted at {datetime.now()}\nImage URL: {image_url}\n")

def job():
    try:
        img, url = fetch_cute_animal_image()
        post_instagram(img)
        post_tiktok(img)
        log_activity(url)
        print("Posted successfully at", datetime.now())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    job()
