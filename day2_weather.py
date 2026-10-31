"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")
city = "Nairobi"

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]

    print(f"Weather in {city}")
    print(f"Temperature: {temp}°C")
    print(f"Condition: {description}")
    print(f"Humidity: {humidity}%")
else:
    print(f"Error: {response.status_code} - {response.text}")

    
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")
city = "Mombasa"  # change this to test

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

try:
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        print(f"Weather in {city}: {temp}\u00B0, {description}, humidity {humidity}%")

    elif response.status_code == 400:
        print(f"Bad request. Chack your parameters. Details: {response.text}")

    elif response.status_code == 401:
        print("API key is invalid or not yet active. Check your .env file.")
    elif response.status_code == 404:
        print(f"City not found: {city}. Check the spelling.")

    elif response.status_code == 500:
        print("Server error on OpenWeather side. Not your fault. Try again later.")

    else:
        print(f"Unexpected error: {response.status_code}")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("Network error: Check your internet connection.")
except requests.exceptions.Timeout:
    print("Request timed out. Try again.")
except Exception as e:
    print(f"Something else went wrong: {e}")