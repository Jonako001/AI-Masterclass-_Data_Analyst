import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("EXCHANGERATE_API_KEY")
print(f"DEBUG: Key loaded? {api_key[:5]}... length {len(api_key) if api_key else 0}")

base = "USD"
target = "KES" # USD to Kenya Shillings - perfect for you in Nairobi

url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base}/{target}"

try:
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()

        if data.get("result") == "success":
            rate = data["conversion_rate"]
            print(f"1 {base} = {rate} {target}")
            print(f"Echange rate USD -> KES: {rate}")

        else:
            print(f"API error: {data.get('error-type')}")
            print("Chack your API key or base currency.")

    elif response.status_code == 401 or response.status_code == 403:

        print("401 Unauthorized: API key invalid. Check .env EXCHANGERATE_API_KEY")

    elif response.status_code == 404:
        print(f"404 Not found: Chack currency code {base} or target")

    elif response.status_code == 429:
        print("429 Too many request. Free tier limit reached. Wait 1 hour.")

    else:
        print(f"Unexpected error: {response.status_code}")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("Network error: Check internet in Nairobi")
except Exception as e:
    print(f"Error: {e}")