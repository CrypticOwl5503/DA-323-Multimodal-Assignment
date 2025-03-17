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

# Visit the main page
MAIN_URL = "https://nationalanthems.info/"
print(f"Opening main page: {MAIN_URL}")
driver.get(MAIN_URL)
wait = WebDriverWait(driver, 10)

# Wait for the page to load
time.sleep(5)


country_links = []
try:

    menu_items = driver.find_elements(By.CSS_SELECTOR, "a.menu-link")
    
    for item in menu_items:
        link = item.get_attribute("href")
        if link and "nationalanthems.info" in link and link != MAIN_URL and ".htm" in link:
            country_links.append(link)

    print(f" Found {len(country_links)} country links.")
except Exception as e:
    print("Error while extracting country links:", e)

# Check if any links were found
if not country_links:
    print(" No country links found. Exiting script.")
    driver.quit()
    exit()

# Directory to save lyrics
LYRICS_DIR = "anthem_lyrics"
os.makedirs(LYRICS_DIR, exist_ok=True)

# Visit each country page and extract the lyrics
for i, country_url in enumerate(country_links):
    try:
        print(f"🔍 Processing [{i+1}/{len(country_links)}]: {country_url}")
        driver.get(country_url)
        time.sleep(3)
        

        country_name = country_url.split("/")[-1].replace(".htm", "")
        
        # Try to find English lyrics
        try:
            english_tab = driver.find_element(By.CSS_SELECTOR, "div.collapseomatic[title='English translation']")
            
            # Getting the ID of the English lyrics tab
            tab_id = english_tab.get_attribute("id")
            
            english_tab.click()
            time.sleep(1)
            
            content_id = "target-" + tab_id
            
            # Get the lyrics content
            lyrics_div = driver.find_element(By.ID, content_id)
            lyrics_content_div = lyrics_div.find_element(By.CSS_SELECTOR, "div[align='left']")
            lyrics_content = lyrics_content_div.text
            
            if lyrics_content:
                # Saving lyrics to file
                lyrics_file = os.path.join(LYRICS_DIR, f"{country_name}_english.txt")
                with open(lyrics_file, 'w', encoding='utf-8') as f:
                    f.write(lyrics_content)
                print(f"Saved English lyrics for {country_name}")
            else:
                print(f"No English lyrics found for {country_name}")
                
        except Exception as e:
            print(f"No English lyrics tab found for {country_name}: {e}")
            
    except Exception as e:
        print(f"Failed to process {country_url}: {e}")

# Close the browser
print("🎉 Script finished. Closing browser.")
driver.quit()
