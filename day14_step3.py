import pandas as pd

august = pd.read_csv("sales_august.csv")
september = pd.read_csv("sales_september.csv")

# Rename - same as before
august = august.rename(columns={"client_name": "customer", "county": "region", "qty": "quantity", "unit_price": "price"})
september = september.rename(columns={"customer_name": "customer"})
august["month"] = "August"
september["month"] = "September"

# STEP 3: Stack them
combined = pd.concat([august, september], ignore_index=True)
print(f"Combined: {len(combined)} rows")
print(combined.groupby("month")["quantity"].sum())

# Add revenue column - this makes Step 4 easy
combined["revenue"] = combined["quantity"] * combined["price"]

# STEP 4: Who grew vs shrank?
monthly = combined.groupby(["month", "customer"])["revenue"].sum().reset_index()
pivot = monthly.pivot(index="customer", columns="month", values="revenue").fillna(0)
pivot["growth"] = pivot["September"] - pivot["August"]
pivot["pct_change"] = ((pivot["September"] - pivot["August"]) / pivot["August"] * 100).round(1)

print("\n--- TOP GROWING ---")
print(pivot.sort_values("pct_change", ascending=False).head(5).to_string())

print("\n--- TOP FALLING / DORMANT ---")
print(pivot.sort_values("pct_change").head(5).to_string())

print("\n--- TOTAL REVENUE ---")
print(combined.groupby("month")["revenue"].sum())
