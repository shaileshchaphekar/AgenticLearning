import requests
import math
from bs4 import BeautifulSoup

def scrape_mumbai_temperature():
    """Scrape the current temperature for Mumbai from Open-Meteo API"""
    try:
        # Using Open-Meteo API (reliable public API, no authentication required)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 19.0760,
            "longitude": 72.8777,
            "current": "temperature_2m",
            "timezone": "Asia/Kolkata"
        }
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        temperature = data["current"]["temperature_2m"]
        return temperature
    except Exception as e:
        print(f"Error scraping temperature: {e}")
        return None

# Scrape temperature for Mumbai
temp = scrape_mumbai_temperature()

if temp is not None:
    print(f"Current temperature in Mumbai: {temp}°C")
    sqrt_temp = math.sqrt(temp)
    print(f"Square root of temperature: {sqrt_temp:.2f}")
else:
    print("Could not retrieve temperature")