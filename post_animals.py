import os
import sys
import requests
from datetime import datetime
from instagrapi import Client
from dotenv import load_dotenv
import traceback

load_dotenv()
print("[DEBUG] Python executable:", sys.executable)

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
        print("[ERROR] Unsplash API error:", resp.text)
        raise e
    data = resp.json()
    img_url = data["urls"]["regular"]
    img_data = requests.get(img_url).content
    filename = f"animal_{datetime.now().strftime('%Y%m%d')}.jpg"
    with open(filename, "wb") as f:
        f.write(img_data)
    print("[DEBUG] Image downloaded:", filename, img_url)
    return filename, img_url

def post_instagram(image_path, caption="Daily dose of cuteness 🐾"):
    """Login with secrets and post to Instagram."""
    cl = Client()
    try:
        cl.login(INSTAGRAM_USER, INSTAGRAM_PASS)
        cl.photo_upload(image_path, caption)
        print("[DEBUG] Instagram upload succeeded")
    except Exception as e:
        print("[ERROR] Instagram upload failed:", e)
        traceback.print_exc()

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
    print("[DEBUG] Log written to", log_file)

def job():
    try:
        img, url = fetch_cute_animal_image()
        post_instagram(img)
        post_tiktok(img)
        log_activity(url)
        print("Posted successfully at", datetime.now())
    except Exception as e:
        print("[ERROR] Job failed:", e)
        traceback.print_exc()

if __name__ == "__main__":
    job()
