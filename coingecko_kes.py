import requests
from datetime import datetime

url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids": "bitcoin,ethereum,solana",
    "vs_currencies": "usd,kes",
    "include_market_cap": "true",
    "include_24hr_change": "true"
}

data = requests.get(url, params=params).json()

print(f"=== Live Crypto Prices — {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")

for coin_id in ["bitcoin", "ethereum", "solana"]:
    info = data[coin_id]
    # Safely get change - try both possible key names
    change = info.get('usd_24h_change') or info.get('usd_24hr_change') or 0
    
    print(f"{coin_id.capitalize()}")
    print(f"  Price: KES {info['kes']:,.2f} (${info['usd']:,.2f})")
    print(f"  24h Change: {change:+.2f}%")
    print()

print(f"Today, 1 Bitcoin = KES {data['bitcoin']['kes']:,.0f}")
print("Source: CoinGecko free API (no key needed)")