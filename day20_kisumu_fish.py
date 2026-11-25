import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import random

random.seed(42)
conn = sqlite3.connect("kisumu_fish.db")

conn.executescript("""
DROP TABLE IF EXISTS transactions;
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    date TEXT,
    vendor_name TEXT,
    fish_type TEXT,
    kg_sold REAL,
    price_per_kg REAL,
    buyer_type TEXT
);
""")

vendors = ["Otieno Fisheries", "Achieng Fresh Fish", "Owino & Sons",
           "Atieno Aquatics", "Ochieng Lake Harvest", "Kamau Fish Traders"]
fish_types = ["Tilapia", "Nile Perch", "Omena", "Catfish", "Silver Cyprinid"]
base_price = {"Tilapia": 420, "Nile Perch": 550, "Omena": 180, "Catfish": 380, "Silver Cyprinid": 200}

# 60 transactions, Jan-Mar 2026
rows = []
for i in range(1, 61):
    vendor = random.choice(vendors)
    fish = random.choice(fish_types)
    kg = round(random.uniform(5, 80), 1)
    buyer = random.choice(["retail", "wholesale"])
    price = base_price[fish] + (60 if buyer == "retail" else -20) + random.randint(-20, 30)
    month = random.choice(["01", "02", "03"])
    day = random.randint(1, 28)
    date = f"2026-{month}-{day:02d}"
    rows.append((i, date, vendor, fish, kg, price, buyer))

conn.executemany("INSERT INTO transactions VALUES (?,?,?,?,?,?,?)", rows)
conn.commit()
print(f"Inserted {len(rows)} rows")

# Q1: Top 3 vendors by revenue
q1 = """
SELECT vendor_name,
       SUM(kg_sold * price_per_kg) AS total_revenue,
       SUM(kg_sold) AS total_kg,
       COUNT(*) AS transactions
FROM transactions
GROUP BY vendor_name
ORDER BY total_revenue DESC
LIMIT 3
"""
df_q1 = pd.read_sql_query(q1, conn)
print("\n--- Q1: Top 3 Vendors ---")
print(df_q1)

# Q2: Wholesale vs Retail - revenue per kg
q2 = """
SELECT buyer_type,
       SUM(kg_sold * price_per_kg) AS total_revenue,
       SUM(kg_sold) AS total_kg,
       SUM(kg_sold * price_per_kg) / SUM(kg_sold) AS revenue_per_kg,
       AVG(price_per_kg) AS avg_price_per_kg
FROM transactions
GROUP BY buyer_type
"""
df_q2 = pd.read_sql_query(q2, conn)
print("\n--- Q2: Wholesale vs Retail per kg ---")
print(df_q2)

# Q3: Revenue trend by month
q3 = """
SELECT strftime('%Y-%m', date) AS month,
       SUM(kg_sold * price_per_kg) AS monthly_revenue,
       SUM(kg_sold) AS monthly_kg
FROM transactions
GROUP BY month
ORDER BY month
"""
df_q3 = pd.read_sql_query(q3, conn)
print("\n--- Q3: Monthly Trend ---")
print(df_q3)

# Chart - one image, two panels
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].bar(df_q1["vendor_name"], df_q1["total_revenue"], color="#1F4E79")
axes[0].set_title("Top 3 Vendors by Revenue (KES)")
axes[0].tick_params(axis="x", rotation=15)
axes[0].set_ylabel("Revenue (KES)")

axes[1].plot(df_q3["month"], df_q3["monthly_revenue"], marker="o", color="#2E75B6", linewidth=2)
axes[1].set_title("Monthly Revenue Trend")
axes[1].set_ylabel("Revenue (KES)")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("kisumu_fish_analysis.png", dpi=150)
print("\nChart saved: kisumu_fish_analysis.png")
conn.close()