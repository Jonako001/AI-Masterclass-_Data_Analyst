"""
import requests

url = "https://restcountries.com/v3.1/name/kenya"

response = requests.get(url)
print("Status code:", response.status_code)
print("Data received:", response.json())

"""
import requests

url = "https://api.restcountries.com/countries/v5?q=kenya&pretty=1"
headers = {
    "Authorization": "Bearer rc_live_73797869c0d248b8ba6f3e43376f7f6c"
}

response = requests.get(url, headers=headers)
print("Status code:", response.status_code)

raw = response.json()
country = raw["data"]["objects"][0]

# New v5 folder system
name = country["names"]["common"]
capital = country["capitals"][0]["name"]
population = country["population"]
currency = country["currencies"][0]["code"]

print(f"Country: {name}")
print(f"Capital: {capital}")
print(f"Population: {population:,}")
print(f"Currency: {currency}")

# Bonus for your class - this is the "folder" lesson
print("\nJSON folders learned:")
print("name = data['objects'][0]['names']['common']")
print("capital = data['objects'][0]['capitals'][0]['name']")