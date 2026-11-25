import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# STEP 1: Create DB
conn = sqlite3.connect("baraka_distributors.db")

conn.executescript("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    date TEXT, product TEXT, county TEXT,
    quantity INTEGER, unit_price INTEGER
);
INSERT OR IGNORE INTO sales VALUES
(1,'2024-01-15','Maize Flour','Nairobi',120,2800),
(2,'2024-01-18','Rice','Kisumu',80,4500),
(3,'2024-02-02','Cooking Oil','Mombasa',55,1800),
(4,'2024-02-14','Maize Flour','Nakuru',90,2800),
(5,'2024-03-01','Rice','Nairobi',110,4500),
(6,'2024-03-12','Wheat Flour','Kisumu',75,3200);
""")
conn.commit()
print("Database ready")

# STEP 2: Revenue by product - SQL -> pandas
query = """
SELECT product,
       SUM(quantity * unit_price) AS total_revenue,
       SUM(quantity) AS total_units,
       COUNT(*) AS order_count
FROM sales
GROUP BY product
ORDER BY total_revenue DESC
"""
df = pd.read_sql_query(query, conn)
print(df)

# STEP 3: County analysis - pandas layer on top of SQL
county_q = """
SELECT county, 
       SUM(quantity * unit_price) AS revenue,
       SUM(quantity) AS units
FROM sales GROUP BY county
"""
county_df = pd.read_sql_query(county_q, conn)

county_df["revenue_share_pct"] = (county_df["revenue"] / county_df["revenue"].sum() * 100).round(1)
county_df = county_df.sort_values("revenue", ascending=False)
print(county_df.to_string(index=False))

# STEP 4: Visualize
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].barh(county_df["county"], county_df["revenue"], color="#1F4E79")
axes[0].set_title("Revenue by County (KES)")
axes[0].set_xlabel("Revenue (KES)")

axes[1].bar(df["product"], df["total_revenue"], color="#2E75B6")
axes[1].set_title("Revenue by Product (KES)")
axes[1].tick_params(axis="x", rotation=20)

plt.tight_layout()
plt.savefig("baraka_analysis.png", dpi=150)
print("Charts saved: baraka_analysis.png")

conn.close()