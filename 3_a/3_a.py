import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


options = webdriver.ChromeOptions()
options.add_argument("--headless") 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


url = "https://hampusborgos.github.io/country-flags/"
driver.get(url)


time.sleep(3) 


flags = driver.find_elements(By.CSS_SELECTOR, "div#flags figure.flag")

save_folder = "flags"
os.makedirs(save_folder, exist_ok=True)

flag_data = []
for flag in flags:
    img_tag = flag.find_element(By.TAG_NAME, "img")
    caption_tag = flag.find_element(By.TAG_NAME, "figcaption")

    if img_tag and caption_tag:
        img_url = img_tag.get_attribute("src")
        country_name = caption_tag.text.strip()
        flag_data.append((country_name, img_url))

# Close Selenium
driver.quit()

# Downloading the first 100 flags
for i, (country_name, img_url) in enumerate(flag_data):
    image_response = requests.get(img_url)

    if image_response.status_code == 200:
        file_path = os.path.join(save_folder, f"{country_name}.svg")
        with open(file_path, "wb") as file:
            file.write(image_response.content)
        print(f"{i+1}. Downloaded: {file_path}")
    else:
        print(f"{i+1}. Failed to download: {img_url}")

print("Download complete!")
