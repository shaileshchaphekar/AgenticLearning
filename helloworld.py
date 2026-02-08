import requests
import math
from bs4 import BeautifulSoup

def scrape_mumbai_temperature():
    """Scrape the current temperature for Mumbai from wttr.in"""
    try:
        # Using wttr.in API (public, no authentication required)
        url = "https://wttr.in/Mumbai?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        temperature = data["current_condition"][0]["temp_C"]
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