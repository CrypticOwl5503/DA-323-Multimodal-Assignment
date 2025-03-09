import os
import time
import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from PIL import Image
from io import BytesIO

# Set up Chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

# Set up Chrome WebDriver
chrome_driver_path = "D:\\Code\\ChromeDriver-134\\chromedriver-win64\\chromedriver.exe"  # Update path
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Categories to search
categories = [
    "Cat", "Dog", "Orange", "Apple", "School", "Bird", "City", "Village", "Bird", "Human",
    "Fruit", "Sky", "Museum", "Ocean", "Sports", "Musical Instruments",
    "Pencil", "Eraser", "Book", "Bottle"
]

# Create a folder for images
os.makedirs("images", exist_ok=True)

# Create/open CSV file for metadata
metadata_file = "image_metadata.csv"
with open(metadata_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Category", "Filename", "URL", "Resolution"])  # Write header

# Function to download images and store metadata
def download_image(url, folder, img_name, category):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            resolution = f"{image.width}x{image.height}"
            file_path = os.path.join(folder, f"{img_name}.jpg")
            image.save(file_path, "JPEG")

            # Store metadata in CSV
            with open(metadata_file, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([category, f"{img_name}.jpg", url, resolution])
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Function to scroll and fetch image URLs
def fetch_image_urls(query, max_images=50):
    search_url = f"https://www.google.com/search?q={query}&tbm=isch"
    driver.get(search_url)
    time.sleep(2)  # Allow initial load

    urls = set()
    
    # Scroll until we have enough images
    while len(urls) < max_images:
        images = driver.find_elements(By.CSS_SELECTOR, "img")
        
        for img in images:
            try:
                src = img.get_attribute("data-src") or img.get_attribute("src")  # Prefer full-size images
                if src and src.startswith("http") and src not in urls:
                    urls.add(src)
                if len(urls) >= max_images:
                    break  # Stop when we reach 50 images
            except Exception as e:
                print(f"Error fetching image source: {e}")
        
        # Scroll down
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        time.sleep(2)

        # Try clicking "Show more results" if available
        try:
            show_more = driver.find_element(By.CSS_SELECTOR, "input[value='Show more results']")
            show_more.click()
            time.sleep(2)
        except:
            pass  # No button available, continue scrolling

    return list(urls)[:max_images]  # Ensure we return exactly 50 images

# Loop through categories and download images
for category in categories:
    print(f"Downloading images for {category}...")
    category_folder = os.path.join("images2", category.replace(" ", "_"))
    os.makedirs(category_folder, exist_ok=True)

    retries = 0
    image_urls = fetch_image_urls(category, max_images=50)

    while len(image_urls) < 50 and retries < 3:  # Retry if less than 50 images
        print(f"Retrying {category}... Attempt {retries + 1}")
        time.sleep(5)
        image_urls = fetch_image_urls(category, max_images=50)
        retries += 1

    if len(image_urls) < 50:
        print(f"Warning: Only {len(image_urls)} images found for {category}.")

    for idx, img_url in tqdm(enumerate(image_urls), total=len(image_urls)):
        download_image(img_url, category_folder, f"{category}_{idx}", category)

# Close the browser
driver.quit()

print("Image downloading complete! Metadata saved in 'image_metadata.csv'.")
