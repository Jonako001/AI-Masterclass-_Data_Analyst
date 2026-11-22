import sqlite3
import pandas as pd

def get_county_orders(conn, county):
    # Safe: county is passed separately, never put inside the SQL string

    query = """
        SELECT o.customer_name AS customer,
               c.county,
               o.quantity * o.unit_price AS total_value
        FROM orders o
        JOIN customers c ON c.customer = o.customer_name
        WHERE c.county = ?
        ORDER BY total_value DESC
    """
    return pd.read_sql_query(query, conn, params=(county,))

conn = sqlite3.connect("distributor.db") # <-- your REAL file

print("--- Mombasa ---")
print(get_county_orders(conn, "Mombasa"))

print("\n--- Kisumu ---")
print(get_county_orders(conn, "Kisumu"))

print("\n--- Nairobi ---")
print(get_county_orders(conn, "Nairobi"))

# Hacker tries to break it:
print(get_county_orders(conn, "' OR 1=1 --"))

conn.close()