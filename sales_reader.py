import csv

CSV_FILE = "sales.csv"

def main():
    total_sales = 0
    top_person = None
    top_amount = 0
    count = 0

    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            amount = float(row["amount"])
            count += 1
            total_sales += amount
            if amount > top_amount:
                top_amount = amount
                top_person = row

    top_name = top_person["name"]
    top_county = top_person["county"]
    top_amt = float(top_person["amount"])

    print("\n=== Sales Data Report ===")
    print(f"Records: {count}")
    print(f"Total sales: KES {total_sales:,.2f}")
    print("-" * 40)
    print(f"Top Salesperson: {top_name}")
    print(f"County: {top_county}")
    print(f"Amount: KES {top_amt:,.2f}")
    print("=" * 40)

if __name__ == "__main__":
    main()