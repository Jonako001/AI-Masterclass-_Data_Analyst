import sqlite3
import pandas as pd

conn = sqlite3.connect("distributor.db")

# Q1: Which county generates the most revenue?
print("--- Q1: Which county generates the most revenue? ---")
q1 = """
SELECT c.county,
       SUM(o.quantity * o.unit_price) AS total_revenue,
       COUNT(*) AS total_orders
FROM orders o
JOIN customers c ON c.customer = o.customer_name
GROUP BY c.county
ORDER BY total_revenue DESC
LIMIT 1
"""
print(pd.read_sql_query(q1, conn))

# Q2: Which customers have placed more than 2 orders?
print("\n--- Q2: Customers with > 2 orders ---")
q2 = """
SELECT customer_name,
       COUNT(*) AS order_count,
       SUM(quantity * unit_price) AS total_spent
FROM orders
GROUP BY customer_name
HAVING COUNT(*) > 2
ORDER BY total_spent DESC
"""
print(pd.read_sql_query(q2, conn))

# Q3: What % of orders are still pending?
print("\n--- Q3: % of orders by status ---")
q3 = """
SELECT status,
       COUNT(*) AS order_count,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders), 1) AS pct
FROM orders
GROUP BY status
"""
print(pd.read_sql_query(q3, conn))

conn.close()