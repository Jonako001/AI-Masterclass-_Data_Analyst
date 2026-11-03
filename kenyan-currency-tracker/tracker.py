import requests
from datetime import datetime

API_URL = "https://api.exchangerate-api.com/v4/latest/KES"
DEMO_RATES = {"USD": 0.007735, "EUR": 0.007122, "GBP": 0.00609}

def get_rates():
    try:
        r = requests.get(API_URL, timeout=8)
        r.raise_for_status()
        data = r.json()
        print("Live rates loaded from exchangerate-api.com!")
        return data["rates"], data["date"], True
    except:
        print("Live API blocked (DNS), using demo rates")
        return DEMO_RATES, "2026-11-02 offline demo", False

def main():
    print("\n=== Kenyan Business Currency Tracker ===")
    rates, date, is_live = get_rates()
    kes_amount = float(input("\nEnter price in KES: ").strip())
    
    usd = kes_amount * rates["USD"]
    eur = kes_amount * rates["EUR"]
    gbp = kes_amount * rates["GBP"]

    print("\n" + "="*50)
    print("QUOTE:", datetime.now().strftime("%Y-%m-%d %H:%M"), "- LIVE" if is_live else "- OFFLINE DEMO")
    print("Rates date:", date)
    print("="*50)
    print(f"KES {kes_amount:,.2f} = USD ${usd:,.2f} / EUR {eur:,.2f} / GBP {gbp:,.2f}")
    print("="*50)

if __name__ == "__main__":
    main()