"""
Travel Weather Tool

Shows weather + country info for any city.
Chains OpenWeatherMap + Countries API.
Handles deprecated REST Countries v3.1.

Usage:
    python day3_travel_info.py
    python day3_travel_info.py Nairobi

Requirements:
    pip install requests python-dotenv
    OPENWEATHER_API_KEY in .env file
"""
import requests
import os
import json
import sys
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            print(f"Weather API error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None

def get_country_info(country_code):
    try:
        url = "https://api.sampleapis.com/countries/countries"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            all_countries = response.json()
            for c in all_countries:
                if c.get("alpha2Code") == country_code or c.get("alpha3Code") == country_code:
                    return {
                        "name": {"common": c.get("name")},
                        "region": c.get("region"),
                        "population": c.get("population"),
                        "currencies": {cur: {} for cur in [c.get("currency")] if cur} if c.get("currency") else {}
                    }
    except Exception as e:
        print(f"Country API failed: {e}")
    
    fallback = {
        "KE": {"name": {"common": "Kenya"}, "region": "Africa", "population": 55100586, "currencies": {"KES": {}}},
        "NG": {"name": {"common": "Nigeria"}, "region": "Africa", "population": 218541212, "currencies": {"NGN": {}}},
        "UG": {"name": {"common": "Uganda"}, "region": "Africa", "population": 47249585, "currencies": {"UGX": {}}},
        "TZ": {"name": {"common": "Tanzania"}, "region": "Africa", "population": 65497748, "currencies": {"TZS": {}}},
        "US": {"name": {"common": "United States"}, "region": "Americas", "population": 340000000, "currencies": {"USD": {}}},
        "GB": {"name": {"common": "United Kingdom"}, "region": "Europe", "population": 67000000, "currencies": {"GBP": {}}},
    }
    return fallback.get(country_code, {"name": {"common": country_code}, "region": "Unknown", "population": 0, "currencies": {}})

def save_to_file(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n[Saved raw data to {filename} for offline use]")

def run_tool():
    print("Travel Weather Tool")
    print("-------------------")
    
    if not api_key:
        print("ERROR: OPENWEATHER_API_KEY not found in .env")
        return

    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:]).strip()
        print(f"Using city: {city}")
    else:
        city = input("Enter a city name: ").strip()

    if not city:
        print("No city entered. Exiting.")
        return

    print(f"\nFetching data for {city}...")
    weather_data = get_weather(city)

    if not weather_data:
        print(f"Could not find weather data for '{city}'. Check spelling.")
        return

    country_code = weather_data["sys"]["country"]
    country_data = get_country_info(country_code)

    print(f"\n=== {city.title()}, {country_code} ===")
    print(f"Temperature : {weather_data['main']['temp']}C")
    print(f"Condition   : {weather_data['weather'][0]['description'].title()}")
    print(f"Humidity    : {weather_data['main']['humidity']}%")
    print(f"Wind        : {weather_data['wind']['speed']} m/s")

    if country_data:
        population = country_data.get("population", 0)
        region = country_data.get("region", "Unknown")
        currencies_dict = country_data.get("currencies", {})
        name_obj = country_data.get("name", {})

        if isinstance(name_obj, dict):
            common_name = name_obj.get('common', country_code)
        else:
            common_name = str(name_obj) if name_obj else country_code

        if currencies_dict:
            currencies = ", ".join(currencies_dict.keys())
        else:
            currencies = "Unknown"

        print(f"\n=== Country Info ({common_name}) ===")
        print(f"Region      : {region}")
        print(f"Population  : {population:,}" if population else "Population  : Unknown")
        print(f"Currency    : {currencies}")
    else:
        print(f"\n[Country info unavailable for {country_code}]")

    save_to_file(weather_data, f"{city.lower()}_weather.json")

if __name__ == "__main__":
    run_tool()