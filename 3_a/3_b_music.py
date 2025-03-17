from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os


CHROMEDRIVER_PATH = "D:\\Code\\ChromeDriver-134\\chromedriver-win64\\chromedriver.exe"
service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

MAIN_URL = "https://nationalanthems.info/"
print(f"Opening main page: {MAIN_URL}")
driver.get(MAIN_URL)
wait = WebDriverWait(driver, 10)


time.sleep(5)

country_links = []
try:

    menu_items = driver.find_elements(By.CSS_SELECTOR, "a.menu-link")
    
    for item in menu_items:
        link = item.get_attribute("href")
        if link and "nationalanthems.info" in link and link != MAIN_URL and ".htm" in link:
            country_links.append(link)

    print(f"Found {len(country_links)} country links.")
except Exception as e:
    print("Error while extracting country links:", e)

# Check if any links were found
if not country_links:
    print("No country links found. Exiting script.")
    driver.quit()
    exit()

# Directory to save MP3 files
DOWNLOAD_DIR = "national_anthems"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

for i, country_url in enumerate(country_links):
    try:
        # Creating MP3 link by replacing .htm with .mp3
        mp3_link = country_url.replace(".htm", ".mp3")
        print(f"Processing [{i+1}/{len(country_links)}]: {country_url}")
        print(f"Generated MP3 link: {mp3_link}")

        headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        anthem_name = country_url.split("/")[-1].replace(".htm", "") + ".mp3"
        anthem_path = os.path.join(DOWNLOAD_DIR, anthem_name)
        
        response = requests.get(mp3_link, headers=headers)
        if response.status_code == 200:
            with open(anthem_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {anthem_name}")
        else:
            print(f"Failed to download {mp3_link}: Status code {response.status_code}")

    except Exception as e:
        print(f"Failed to process {country_url}: {e}")

# Closing the browser
print("Script finished. Closing browser.")
driver.quit()
