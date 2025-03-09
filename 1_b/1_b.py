import os
import requests
from bs4 import BeautifulSoup
import csv
import time
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

# Ensure necessary nltk data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Define categories and websites
categories = {
    "Football": ["https://www.goal.com/", "https://www.espn.com/soccer/", "https://www.fifa.com/"],
    "Chess": ["https://www.chess.com/", "https://lichess.org/blog", "https://www.fide.com/"],
    "Science": ["https://www.sciencenews.org/", "https://www.nature.com/", "https://www.livescience.com/"],
    "Education": ["https://www.edutopia.org/", "https://www.teachthought.com/", "https://www.khanacademy.org/"],
    "India": ["https://www.thehindu.com/", "https://timesofindia.indiatimes.com/", "https://indianexpress.com/"],
    "China": ["https://www.scmp.com/", "https://www.globaltimes.cn/", "https://www.chinadaily.com.cn/"],
    "Artificial Intelligence": ["https://www.analyticsvidhya.com/", "https://www.aitrends.com/", "https://www.deepmind.com/"],
    "Politics": ["https://www.politico.com/", "https://www.npr.org/sections/politics/", "https://www.aljazeera.com/tag/politics/"],
    "Travel": ["https://www.lonelyplanet.com/", "https://www.nomadicmatt.com/", "https://www.roughguides.com/"],
    "Movies": ["https://www.rottentomatoes.com/", "https://www.imdb.com/news/movie/", "https://www.hollywoodreporter.com/"],
    "Finance": ["https://www.investopedia.com/", "https://www.bloomberg.com/", "https://www.cnbc.com/finance/"],
    "TV Shows": ["https://www.tvguide.com/", "https://www.digitalspy.com/tv/", "https://www.avclub.com/tv"],
    "Photography": ["https://petapixel.com/", "https://www.dpreview.com/", "https://fstoppers.com/"],
    "Health": ["https://www.healthline.com/", "https://www.webmd.com/", "https://www.mayoclinic.org/"],
    "History": ["https://www.history.com/", "https://www.bbc.co.uk/history", "https://www.nationalgeographic.com/history/"],
    "Weather": ["https://www.weather.com/", "https://www.accuweather.com/", "https://www.noaa.gov/"],
    "Geography": ["https://www.worldatlas.com/", "https://www.nationalgeographic.com/maps/", "https://geology.com/"],
    "Fashion": ["https://www.vogue.com/", "https://www.elle.com/", "https://www.gq.com/"],
    "Food": ["https://www.foodnetwork.com/", "https://www.seriouseats.com/", "https://www.bonappetit.com/"],
    "Business": ["https://www.forbes.com/", "https://hbr.org/", "https://www.businessinsider.com/"]
}

# Function to clean text
def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    tokens = word_tokenize(text)  # Tokenize text
    stop_words = set(stopwords.words("english"))  # Get stop words
    cleaned_text = " ".join([word for word in tokens if word not in stop_words])  # Remove stopwords
    return cleaned_text

# Function to scrape articles
def scrape_category(category, urls):
    text_data = []
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract title, content, and date if available
            title = soup.title.string if soup.title else "No Title"
            content = " ".join([p.text for p in soup.find_all("p")])
            cleaned_content = clean_text(content)

            text_data.append(f"Title: {title}\nContent: {cleaned_content}\n\n")
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    return text_data

# Create text files for each category
for category, urls in categories.items():
    print(f"Scraping {category}...")
    articles = scrape_category(category, urls)
    
    with open(f"{category}.txt", "w", encoding="utf-8") as file:
        file.writelines(articles)

print("Scraping complete! Data saved to text files.")
