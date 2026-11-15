import pandas as pd
import random

random.seed(14)
customers_aug = ["Kamau Stores", "Otieno Wholesale", "Hassan Traders", "Wanjiku Shop", "Mombasa Board Ltd", "Kilifi Traders", "Njoroge Mart", "Amina Supplies", "Baraka Wholesalers", "Chebet Store"]
customers_sep = ["Kamau Stores", "Otieno Wholesale", "Hassan Traders", "Wanjiku Shop", "Mombasa Board Ltd", "Kilifi Traders", "Njoroge Mart", "Amina Supplies"] # 2 dropped = dormant

products = ["Rice 25kg", "Cooking Oil 5L", "Sugar 10kg", "Maize Flour 5kg"]
counties = ["Mombasa", "Kilifi", "Kwale", "Nairobi", "Kisumu"]

def make_rows(customers, month_num, n, aug_style):
    rows = []
    for i in range(n):
        cust = random.choice(customers)
        qty = random.randint(5, 60)
        price = random.choice([800, 1200, 1500, 2200])
        rows.append({
            "date": f"2026-{month_num:02d}-{random.randint(1,28):02d}",
            "client_name" if aug_style else "customer_name": cust,
            "county" if aug_style else "region": random.choice(counties),
            "product": random.choice(products),
            "qty" if aug_style else "quantity": qty,
            "unit_price" if aug_style else "price": price
        })
    return pd.DataFrame(rows)

august = make_rows(customers_aug, 8, 243, True)
september = make_rows(customers_sep, 9, 198, False)

august.to_csv("sales_august.csv", index=False)
september.to_csv("sales_september.csv", index=False)
print("Done! Files created.")
print(august.head(2).to_string())