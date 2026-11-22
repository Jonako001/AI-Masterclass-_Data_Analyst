import sqlite3
import pandas as pd

conn = sqlite3.connect("distributor.db") # your REAL file

# Load, clean and write back
df = pd.read_sql_query("SELECT * FROM orders", conn)
print(f"Loaded: {df.shape}")
print("Columns:", list(df.columns))

# 1. Create total_value first - it doesn't exist yet!
df['total_value'] = df['quantity'] * df['unit_price']

# 2. Add a calculated column
df['revenue_category'] = df['total_value'].apply(
    lambda x: 'high' if x > 50000 else ('mid' if x >15000 else 'low')
)

print("\n--- Categories ---")
print(df['revenue_category'].value_counts())

# 3. Write to a NEW table in the same database
df.to_sql('orders_enriched', conn, if_exists='replace', index=False)
print("\nWritten to orders_enriched.")

# 4. Confirm it is there
check = pd.read_sql_query("SELECT * FROM orders_enriched LIMIT 5", conn)
print(check[['customer_name', 'total_value', 'revenue_category']])


conn.close()