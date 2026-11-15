import pandas as pd

august = pd.read_csv("sales_august.csv")
september = pd.read_csv("sales_september.csv")

print("BEFORE:")
print("August columns:", august.columns.tolist())
print("September columns:", september.columns.tolist())

# Step 1: Rename to standard format
august = august.rename(columns={
    "client_name": "customer",
    "county": "region",
    "qty": "quantity",
    "unit_price": "price"
})

september = september.rename(columns={
    "customer_name": "customer"
})

# Step 2: Add month column
august["month"] = "August"
september["month"] = "September"

print("\nAFTER:")
print("August columns:", august.columns.tolist())
print("September columns:", september.columns.tolist())
print(august["price"].dtype, september["price"].dtype)
print(f"August: {len(august)} rows | September: {len(september)} rows")