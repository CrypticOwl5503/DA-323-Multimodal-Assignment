import requests
import pandas as pd
import time

API_KEY = "c62745e003e66f8f138461a1333d6364"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

CITIES = [
    "Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Jaipur",
    "Ahmedabad", "Lucknow", "Chandigarh", "Bhopal", "Indore", "Patna", "Surat", "Nagpur",
    "Kochi", "Bhubaneswar", "Guwahati", "Dehradun"
]

def fetch_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    
    # Trying 3 times
    for attempt in range(3): 
        try:
            response = requests.get(BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return {
                "City": city,
                "Temperature (°C)": data["main"]["temp"],
                "Humidity (%)": data["main"]["humidity"],
                "Wind Speed (m/s)": data["wind"]["speed"],
                "Timestamp": pd.Timestamp.now()
            }
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1}: Failed to fetch data for {city} - {e}")
            time.sleep(5)
    print(f"Skipping {city} after 3 failed attempts.")
    return None

# Collecting weather data
weather_data = [fetch_weather(city) for city in CITIES]
weather_data = [w for w in weather_data if w is not None]

# Converting to DataFrame and Saving
df = pd.DataFrame(weather_data)
df.to_csv("india_weather_data.csv", index=False)

print("Weather data saved successfully!")
