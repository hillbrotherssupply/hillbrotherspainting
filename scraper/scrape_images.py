import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# ==== CONFIG ====
HTML_FILE = "contractors.html"  # or contractors page
OUTPUT_FOLDER = "images/contractors"
BASE_URL = ""  # e.g. "https://hillbrothersnh.com/"

# ==== SETUP ====
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

with open(HTML_FILE, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

image_urls = set()

# ==== 1. Collect every possible image source ====
# Regular and lazy-loaded <img> tags (including carousels)
for img in soup.find_all("img"):
    for attr in ["src", "data-src", "data-original"]:
        src = img.get(attr)
        if src:
            image_urls.add(urljoin(BASE_URL, src))

# <source srcset>
for source in soup.find_all("source"):
    srcset = source.get("srcset")
    if srcset:
        src = srcset.split(",")[0].strip().split(" ")[0]
        image_urls.add(urljoin(BASE_URL, src))

# Inline CSS background-image
for tag in soup.find_all(style=True):
    matches = re.findall(r'url\(([^)]+)\)', tag["style"])
    for match in matches:
        cleaned = match.strip(' "\'')
        image_urls.add(urljoin(BASE_URL, cleaned))

print(f"Found {len(image_urls)} potential image URLs.")

# ==== 2. Download each image ====
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://www.wix.com/"
}

for img_url in image_urls:
    # Skip data URLs
    if img_url.startswith("data:"):
        continue

    # Fix Wix URLs (remove transformation path)
    if "wixstatic.com/media/" in img_url and "/v1/" in img_url:
        img_url = img_url.split("/v1/")[0]

    filename = os.path.basename(urlparse(img_url).path)
    if not filename:
        filename = f"image_{abs(hash(img_url))}.jpg"
    filepath = os.path.join(OUTPUT_FOLDER, filename)

    try:
        response = requests.get(img_url, stream=True, timeout=10, headers=headers)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
        print(f"✅ Downloaded: {filename}")
    except Exception as e:
        print(f"❌ Failed {img_url}: {e}")

print("\n✅ Done. Check the 'images/' folder.")
