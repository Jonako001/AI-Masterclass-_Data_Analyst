"""
Dairy  Co-op Payment Calculator
Farmer enters name and litres. Tool shows total owed.
Usage: python day10_dairy_calculator.py
config: Edit price.text to update weekly rate.
"""

def get_current_price():
    try:
        with open("price.text", "r") as f:
            return float(f.read().strip())
    except FileNotFoundError:
        return 55.0

def calculate_payment(litres, price_per_litre):
    return litres * price_per_litre

def run():
    print("Kiambu Dairy Co-op Payment Calculator")
    print("--------------------------------------")
    print(f"Current buying price: KES {get_current_price():.2f} per litre\n")

    name = input("Farmer name: ").strip()
    if not name:
        print("Name is required.")
        return

    try:
        litres = float(input("Litres supplied today: "))
        if litres <= 0:
            print("Litres must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid number for litres.")
        return

    price = get_current_price()
    total = calculate_payment(litres, price)

    print(f"\nFarmer : {name}")
    print(f"Litres : {litres}")
    print(f"Price  : KES {price:.2f}/litre")
    print(f"Total  : KES {total:,.2f}")

run()