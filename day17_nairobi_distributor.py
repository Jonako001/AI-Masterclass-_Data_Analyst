import sqlite3
import pandas as pd

# Connect to your database - change this path to your file
conn = sqlite3.connect("distributor.db")

# --- (1) JOIN: Each order with the customer's account tier ---
# Answers: "Which tier is buying what?"
query1 = """
SELECT
  o.order_id,
  o.customer_name,
  c.county,
  c.account_tier,
  o.quantity * o.unit_price AS total_value
FROM orders o
JOIN customers c ON c.customer = o.customer_name
ORDER BY total_value DESC;
"""

# --- (2) Total spend per customer, only customers with MORE than 3 orders ---
# Answers: "Who are our loyal, repeat buyers?"
query2 = """
SELECT
  o.customer_name,
  c.county,
  c.account_tier,
  COUNT(o.order_id) AS order_count,
  SUM(o.quantity * o.unit_price) AS total_spend
FROM orders o
JOIN customers c ON c.customer = o.customer_name
GROUP BY o.customer_name
HAVING COUNT(o.order_id) > 3
ORDER BY total_spend DESC;
"""

# --- (3) Top customer per county using a window function ---
# Answers: "Who is the #1 customer in EACH county?"
query3 = """
SELECT county, customer_name, total_spend
FROM (
  SELECT
    c.county,
    o.customer_name,
    SUM(o.quantity * o.unit_price) AS total_spend,
    ROW_NUMBER() OVER (PARTITION BY c.county ORDER BY SUM(o.quantity * o.unit_price) DESC) AS rank_in_county
  FROM orders o
  JOIN customers c ON c.customer = o.customer_name
  GROUP BY c.county, o.customer_name
)
WHERE rank_in_county = 1
ORDER BY total_spend DESC;
"""

for i, q in enumerate([query1, query2, query3], 1):
    print(f"\n--- QUERY {i} ---")
    df = pd.read_sql_query(q, conn)
    print(df.to_string(index=False))
    print(f"Rows: {len(df)}")

conn.close()