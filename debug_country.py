import requests

country_code = "KE"
urls = [
    f"https://restcountries.com/v3.1/alpha/{country_code}",
    f"https://restcountries.com/v3.1/alpha/{country_code}?fields=name,region,population,currencies",
    f"https://restcountries.com/v3.1/alpha?codes={country_code}"
]

for url in urls:
    print(f"\nTrying: {url}")
    try:
        r = requests.get(url, timeout=10)
        print(f"Status: {r.status_code}")
        data = r.json()
        print(f"Type: {type(data)}")
        print(f"Data preview: {str(data)[:500]}")
    except Exception as e:
        print(f"Error: {e}")