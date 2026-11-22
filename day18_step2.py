import sqlite3
import pandas as pd

conn = sqlite3.connect("distributor.db") # <-- your REAL file, not sales.db


query = """
    SELECT c.county,
           COUNT(*) AS order_count,
           SUM(o.quantity * o.unit_price) AS total_revenue
    FROM orders o
    JOIN customers c ON c.customer = o.customer_name
    GROUP BY c.county
    ORDER BY total_revenue DESC
"""
df = pd.read_sql_query(query, conn)
print(df)
print(df.shape)
conn.close()