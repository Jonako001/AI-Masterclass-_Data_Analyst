import sqlite3
import pandas as pd

conn = sqlite3.connect("distributor.db")

# ========== STEP 2: Your 3 business questions ==========

print("--- Q1: Which county generates the most revenue? ---")
q1 = """
SELECT c.county,
       SUM(o.quantity * o.unit_price) AS total_revenue
FROM orders o
JOIN customers c ON c.customer = o.customer_name
GROUP BY c.county
ORDER BY total_revenue desc
"""
print(pd.read_sql_query(q1, conn))

print("\n--- Q2: Customer with > 2 orders ---")
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

print("\n--- Q3: % of orders by status ---")
q3 = """
SELECT status,
       COUNT(*) AS order_count,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders), 1) AS pct
FROM orders
GROUP BY status
"""
print(pd.read_sql_query(q3, conn))

# HAVING example from lesson: Counties > KES 30,000
print("\n--- BONUS: Counties with > KES 30,000 revenue (HAVING) ---")
q_having = """
SELECT c.county, SUM(o.quantity * o.unit_price) AS total
FROM orders o
JOIN customers c ON c.customer = o.customer_name
GROUP BY c.county
HAVING SUM(o.quantity * o.unit_price) > 30000
ORDER BY total DESC
"""
print(pd.read_sql_query(q_having, conn))

# ========== STEP 3: RANK() - Window function ==========
print("\n--- STEP 3: Rank orders by value WITHIN each county ---")
q_rank = """
SELECT o.customer_name AS customer,
       c.county,
       (o.quantity * o.unit_price) AS total_value,
       RANK() OVER (PARTITION BY c.county ORDER BY (o.quantity * o.unit_price) DESC) AS rank_in_county
FROM orders o
JOIN customers c ON c.customer = o.customer_name
ORDER BY c.county, rank_in_county
"""
print(pd.read_sql_query(q_rank, conn))

# ========== STEP 4: No more SELECT * ==========
print("\n--- STEP 4: Specific columns only ---")
# Lazy: SELECT * FROM orders
# Correct:
q_specific = """
SELECT customer_name, quantity, unit_price
FROM orders
"""
print(pd.read_sql_query(q_specific, conn).head())

# ========== STEP 5: EXPLAIN QUERY PLAN + Index ==========
print("\n--- STEP 5: Before index ---")
for row in conn.execute("EXPLAIN QUERY PLAN SELECT customer_name FROM orders WHERE customer_name = 'Hassan Traders'"):
    print(row)
# Create index on the column you filter by
conn.execute("CREATE INDEX IF NOT EXISTS idx_customer_name ON orders(customer_name)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_county ON customers(county)")
conn.commit()

print("\n--- STEP 5: After index ---")
for row in conn.execute("EXPLAIN QUERY PLAN SELECT customer_name FROM orders WHERE customer_name = 'Hassan Traders'"):
    print(row)

conn.close()
print("\nDone - Day 19 complete")