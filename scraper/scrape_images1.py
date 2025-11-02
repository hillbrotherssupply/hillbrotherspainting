import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Path to your HTML file
HTML_FILE = "hillbrotherspainting_contractors_page.html"
# Output folder for images
OUTPUT_FOLDER = "images"

# Create folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Read and parse HTML
with open(HTML_FILE, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Find all image tags
img_tags = soup.find_all("img")

for img in img_tags:
    src = img.get("src")
    if not src:
        continue

    # Handle relative URLs by resolving them to absolute paths if needed
    base_url = ""  # You can put the base site URL here if the HTML uses relative paths
    img_url = urljoin(base_url, src)

    # Derive filename from URL
    filename = os.path.basename(urlparse(img_url).path)
    if not filename:
        filename = "image_" + str(abs(hash(img_url))) + ".jpg"

    file_path = os.path.join(OUTPUT_FOLDER, filename)

    try:
        response = requests.get(img_url, stream=True, timeout=10)
        response.raise_for_status()
        with open(file_path, "wb") as out_file:
            for chunk in response.iter_content(1024):
                out_file.write(chunk)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")
