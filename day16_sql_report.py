import sqlite3
import pandas as pd

# 1. CREATE DATABASE + TABLE
conn = sqlite3.connect("distributor.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    county TEXT,
    product TEXT,
    quantity INTEGER,
    unit_price REAL,
    order_date TEXT,
    status TEXT
)
""")

# 2. INSERT 20 REALISTIC ROWS
# quantity * unit_price = total_value, we calculate it in the queries
orders_data = [
    (1, 'Kamau Stores', 'Nairobi', 'Maize Flour 2kg', 50, 120, '2026-11-02', 'delivered'),
    (2, 'Otieno Shop', 'Kisumu', 'Rice 25kg', 20, 3200, '2026-11-02', 'delivered'),
    (3, 'Njoroge Supplies', 'Nakuru', 'Cooking Oil 5L', 30, 1450, '2026-11-03', 'pending'),
    (4, 'Hassan Traders', 'Mombasa', 'Rice 25kg', 40, 3200, '2026-11-03', 'delivered'),
    (5, 'Waweru Ltd', 'Nairobi', 'Sugar 1kg', 200, 115, '2026-11-04', 'pending'),
    (6, 'Karanja Mart', 'Mombasa', 'Maize Flour 2kg', 100, 120, '2026-11-04', 'pending'),
    (7, 'Mutua Wholesale', 'Machakos', 'Sugar 1kg', 150, 115, '2026-11-05', 'pending'),
    (8, 'Kiprono Duka', 'Eldoret', 'Cooking Oil 5L', 25, 1450, '2026-11-05', 'delivered'),
    (9, 'Ochieng MiniMart', 'Kisumu', 'Sugar 1kg', 80, 115, '2026-11-06', 'delivered'),
    (10, 'Owino General', 'Nairobi', 'Beans 5kg', 40, 850, '2026-11-06', 'delivered'),
    (11, 'Amina Stores', 'Mombasa', 'Cooking Oil 5L', 60, 1450, '2026-11-09', 'pending'),
    (12, 'Mwangi Retail', 'Nakuru', 'Rice 25kg', 15, 3200, '2026-11-09', 'delivered'),
    (13, 'Chebet Shop', 'Eldoret', 'Maize Flour 2kg', 80, 120, '2026-11-10', 'pending'),
    (14, 'Ali Wholesale', 'Mombasa', 'Sugar 1kg', 300, 115, '2026-11-10', 'delivered'),
    (15, 'Njeri Duka', 'Kiambu', 'Beans 5kg', 60, 850, '2026-11-11', 'pending'),
    (16, 'Baraka Traders', 'Mombasa', 'Rice 25kg', 30, 3200, '2026-11-11', 'pending'),
    (17, 'Kiprop Stores', 'Nakuru', 'Sugar 1kg', 120, 115, '2026-11-12', 'delivered'),
    (18, 'Fatuma Mart', 'Mombasa', 'Maize Flour 2kg', 150, 120, '2026-11-12', 'delivered'),
    (19, 'Onyango Shop', 'Kisumu', 'Cooking Oil 5L', 45, 1450, '2026-11-13', 'pending'),
    (20, 'Wanjiru Wholesale', 'Nairobi', 'Rice 25kg', 25, 3200, '2026-11-13', 'pending'),
]

cursor.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?,?)", orders_data)
conn.commit()

def show(title, query):
    print("\n" + "="*50)
    print(title)
    print("="*50)
    df = pd.read_sql_query(query, conn)
    print(df.to_string(index=False))

# Q1: All orders from Mombasa county
show("Q1: All orders from Mombasa", """
SELECT order_id, customer_name, product, quantity, quantity * unit_price AS total_value, status
FROM orders
WHERE county = 'Mombasa'
ORDER BY order_date
""")

# Q2: Top 10 orders by total value
show("Q2: Top 10 orders by total value", """
SELECT order_id, customer_name, county, product, quantity, quantity * unit_price AS total_value
FROM orders
ORDER BY total_value DESC
LIMIT 10
""")

# Q3: Total revenue per county
show("Q3: Total revenue per county", """
SELECT county, COUNT(*) AS order_count, SUM(quantity * unit_price) AS total_revenue
FROM orders
GROUP BY county
ORDER BY total_revenue DESC
""")

# Q4: All pending orders over KES 50,000
show("Q4: Pending orders over KES 50,000", """
SELECT order_id, customer_name, county, product, quantity * unit_price AS total_value, status
FROM orders
WHERE status = 'pending' AND quantity * unit_price > 50000
ORDER BY total_value DESC
""")

# Q5: Three best-selling products by quantity
show("Q5: Top 3 best-selling products by quantity", """
SELECT product, COUNT(*) AS order_count, SUM(quantity) AS total_units, SUM(quantity * unit_price) AS total_revenue
FROM orders
GROUP BY product
ORDER BY total_units DESC
LIMIT 3
""")

conn.close()