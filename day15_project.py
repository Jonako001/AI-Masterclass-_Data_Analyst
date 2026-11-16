import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("charts", exist_ok=True)
os.makedirs("data", exist_ok=True)

# --- STEP 1: Load + Clean FIRST, then combine ---
august = pd.read_csv("sales_august.csv")
september = pd.read_csv("sales_september.csv")

# Fix August names
august = august.rename(columns={
    "client_name": "customer", 
    "county": "region",
    "qty": "quantity",
    "unit_price": "price"
})

# Fix September names
september = september.rename(columns={
    "customer_name": "customer"
})

august["month"] = "August"
september["month"] = "September"

df =pd.concat([august, september], ignore_index=True)
df["revenue"] = df["quantity"] * df["price"]

print(f"Combined: {len(df)} rows | Total revenue: KES {int(df['revenue'].sum()):,}")
print(df.groupby("month")["revenue"].sum())

# --- STEP 2: Transform - Tiers for YOUR scale ---
def tier(rev):
    if rev >= 1500000:  return "High"
    elif rev >= 800000: return "Medium"
    else: return "Low"

customer_totals = df.groupby("customer")["revenue"].sum().reset_index()
customer_totals["tier"] = customer_totals["revenue"].apply(tier)
print("\nCustomer Tiers:")
print(customer_totals["tier"].value_counts())
print(customer_totals.sort_values("revenue", ascending=False).head(5).to_string())

# Month-over-month per customer for findings
monthly_cust = df.groupby(["month", "customer"])["revenue"].sum().reset_index()
pivot = monthly_cust.pivot(index="customer", columns="month", values="revenue").fillna(0)
pivot["growth"] = pivot["September"] - pivot["August"]
dormant = pivot[(pivot["August"] > 0) & (pivot["September"] == 0)]
print(f"\nDormant customers: {len(dormant)} | Lost revenue: KES {int(dormant['August'].sum()):,}")
print(dormant)

# --- STEP 3: 3 Charts ---
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Chart 1: Revenue by Region
region_rev = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
region_rev.plot(kind="bar", ax=axes[0], color="#1F4E79")
axes[0].set_title("Revenue by Region (Aug-Sep)")
axes[0].set_ylabel("KES")
axes[0].tick_params(axis='x', rotation=30)

# Chart 2: Month-over-month - FIX ORDER (August first)
monthly = df.groupby("month")["revenue"].sum().reindex(["August", "September"])
monthly.plot(kind="bar", ax=axes[1], color=["#1F4E79", "#4472C4"])
axes[1].set_title("Revenue: August vs September")
axes[1].tick_params(axis='x', rotation=0)

# Chart 3: Customer Tier Distribution
customer_totals["tier"].value_counts().plot(kind="pie", ax=axes[2], autopct="%.0f%%")
axes[2].set_title("Customer Revenue Tiers")
axes[2].set_ylabel("")

plt.tight_layout()
plt.savefig("charts/project_analysis.png", dpi=150)
print("\nCharts saved to charts/project_analysis.png")
# plt.show()