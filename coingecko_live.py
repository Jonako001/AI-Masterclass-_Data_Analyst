import requests

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "ids": "bitcoin,ethereum,solana",
    "order": "market_cap_desc",
    "per_page": 3,
    "page": 1
}

response = requests.get(url, params=params)
print(f"Status code: {response.status_code}")

if response.status_code != 200:
    print("ERROR BODY:", response.text[:500])
    print("\nThis means your params are wrong. Check vs_currency and ids.")
    exit()

data = response.json()

print("\n=== Live Crypto Summary ===\n")
for coin in data:
    print(f"{coin['name']} ({coin['symbol'].upper()})")
    print(f"  Price: ${coin['current_price']:,.2f}")
    print(f"  24h Change: {coin['price_change_percentage_24h']:+.2f}%")
    print()