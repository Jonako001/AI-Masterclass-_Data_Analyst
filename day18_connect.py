import sqlite3
import pandas as pd

# YOUR filr is distributor.db, not sales.db
conn = sqlite3.connect("distributor.db") # <-- your REAL file

# Quick check: print all table names
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())
# Expected: [('customers',), ('orders',)]

# Load orders + customers into ONE DataFrame
df = pd.read_sql_query("""
  SELECT o.order_id, o.customer_name, c.account_tier,
         o.quantity * o.unit_price AS total_value
  FROM orders o
  JOIN customers c ON c.customer = o.customer_name
""", conn)

print(df)
print(df.shape) # Should be (5, 5) - 5 orders, 5 columns

conn.close()