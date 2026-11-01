"""
day3_weather_now.py - Live City Weather Tool

Problem it solves: Quickly get accurate, live weather for any city without opening a browser.

How to run:
1. Install requests: pip install requests
2. Run: python day3_weather_now.py
3. Type a city when asked, e.g., Nairobi, Mombasa, Kisumu, London

Requirements met:
- takes user input (city name)
- 2 API calls: Geocoding + Weather (open-meteo.com - free, no API key)
- Saves combined response to JSON file
- Prints clean readable output
- Handles error cases gracefully
- This docstring explains how to run it

APIs used:
- https://geocoding-api.open-meteo.com/v1.search
- https://api.open-meteo.com/v1/forecast
"""


import requests
import json
import sys
from datetime import datetime

def get_coordinates(city_name):
    """API Call 1: Covert city name to latitude/longitude"""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if not data.get("results"):
        return None

    result = data["results"][0]
    return {
        "name": result["name"],
        "country": result["country"],
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "timezone": result.get("timezone", "UTC")
    }

def get_weather(lat, lon):
    """API Calls 2: Get live weather for coordinates"""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,weather_code,relative_humidity_2m,apparent_temperature&daily=sunrise,sunset&timezone=auto"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

def weather_code_to_text(code):
    codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Fog", 51: "Light drizzle", 61: "Slight rain",
        71: "Slight snow", 80: "Slight showers", 95: "Thunderstorm"
    }
    return codes.get(code, f"Weather code {code}")

def main():
    print("\n=== Weather Now - Live Weather Tool ===\n")
    city = input("Enter city name (e.g., Nairobi): ").strip()

    if not city:
        print("Error: You didn't enter a city name. Please try again.")
        sys.exit(1)

    try:
        print(f"nSearching for '{city}'...")
        location = get_coordinates(city)

        if not location:
            print(f"\nSorry, I couldn't find a city called '{city}'.")
            print("Tip: Try checking the spelling, e.g, Nairobi, Mombasa, Kisumu.")
            sys.exit(1)

        print(f"Found: {location['name']}, {location['country']}")
        print("Fetching live weather...")

        weather_data = get_weather(location['latitude'], location['longitude'])

        # Combine results
        combined = {
            "query": city,
            "location_found": location,
            "weather_fetched_at": datetime.now().isoformat(),
            "live_weather": weather_data
        }

        # Save to JSON
        filename = "weather_output_json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)


        # Clean readable output
        current = weather_data.get("current", {})
        daily = weather_data.get("daily", {})


        print("\n" + "="*40)
        print(f"  WEATHER FOR {location['name'].upper()}, {location['country'].upper()}")
        print("="*40)
        print(f"Temperature: {current.get('temperature_2m')}°C (feels like {current.get('apparent_temperature')}°C)")
        print(f"Condition: {weather_code_to_text(current.get('weather_code'))}")
        print(f"Humidity: {current.get('relative_humidity_2m')}%")
        print(f"Wind: {current.get('wind_speed_10m')} km/h")
        if daily.get("sunrise"):
            print(f"Sunrise: {daily['sunrise'][0].split('T')[1]} | Sunset: {daily['sunset'][0].split('T')[1]}")
        print("="*40)
        print(f"\nFull data saved to {filename}")

    except requests.exceptions.ConnectionError:
        print("\nError: No internet connection. Please check your Wi-Fi and try agin.")
    except requests.exceptions.Timeout:
        print("\nError: The weather service is taking too long. Try again in a minute.")
    except requests.exceptions.HTTPError as e:
        print(f"\nError: Weather service failed ({e}). Try again later.")
    except Exception as e :
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    main()