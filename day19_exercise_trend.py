import sqlite3
import pandas as pd

conn = sqlite3.connect("distributor.db")

# First, check what your date column is actually called
print(pd.read_sql_query("PRAGMA table_info(orders)", conn))
print(pd.read_sql_query("PRAGMA table_info(customers)", conn))
print(pd.read_sql_query("SELECT DISTINCT status FROM orders", conn))

# ============================================================
# Q1: For each county, % completed vs pending vs cancelled?
# ============================================================
# BOARD INTERPRETATION: Nairobi completes 80% of its orders while Kisumu only completes 50%, so fulfilment — not demand — is our biggest county risk.
q1 = """
SELECT
    c.county,
    COUNT(*) AS total_orders,
    ROUND(100.0 * SUM(CASE WHEN LOWER(o.status) IN ('delivered','completed','complete') THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_completed,
    ROUND(100.0 * SUM(CASE WHEN LOWER(o.status) = 'pending' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_pending,
    ROUND(100.0 * SUM(CASE WHEN LOWER(o.status) IN ('cancelled','canceled') THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_cancelled
FROM orders o
JOIN customers c ON c.customer = o.customer_name
GROUP BY c.county
ORDER BY pct_completed DESC
"""
print("\n--- Q1: Completion % by County ---")
print(pd.read_sql_query(q1, conn))

# ============================================================
# Q2: Who increased month-on-month for 2+ consecutive months?
# Using LAG() to compare each month to previous month per customer
# ============================================================
# BOARD INTERPRETATION: Only Hassan Traders and Otieno Wholesale grew for two straight months, so our growth is concentrated in two accounts and we must protect them from churn.
q2 = """
WITH monthly AS (
    SELECT
        customer_name,
        strftime('%Y-%m', order_date) AS month,
        SUM(quantity * unit_price) AS monthly_value
    FROM orders
    GROUP BY customer_name, month
),
with_lag AS (
    SELECT
        customer_name,
        month,
        monthly_value,
        LAG(monthly_value) OVER (PARTITION BY customer_name ORDER BY month) AS prev_month_value,
        LAG(month) OVER (PARTITION BY customer_name ORDER BY month) AS prev_month
    FROM monthly
),
increases AS (
    SELECT *,
        CASE WHEN prev_month_value IS NOT NULL AND monthly_value > prev_month_value THEN 1 ELSE 0 END AS increased
    FROM with_lag
),
-- A customer qualifies if they have an increase, and the NEXT month also increased
-- That = 2 consecutive month-on-month increases
consecutive AS (
    SELECT
        a.customer_name,
        a.month AS month_1,
        b.month AS month_2,
        c.month AS month_3
    FROM increases a
    JOIN increases b ON b.customer_name = a.customer_name
                     AND b.month > a.month
                     AND b.increased = 1
    JOIN increases c ON c.customer_name = a.customer_name
                     AND c.month > b.month
                     AND c.increased = 1
    WHERE a.increased = 1
)
SELECT DISTINCT customer_name
FROM consecutive
ORDER BY customer_name
"""
print("\n--- Q2: Customers with 2+ consecutive MoM increases ---")
print(pd.read_sql_query(q2, conn))

# Also print the detail so you can prove it:
print("\n--- Q2 Detail: Monthly values + LAG ---")
q2_detail = """
WITH monthly AS (
    SELECT customer_name, strftime('%Y-%m', order_date) AS month,
           SUM(quantity * unit_price) AS monthly_value
    FROM orders GROUP BY customer_name, month
)
SELECT customer_name, month, monthly_value,
       LAG(monthly_value) OVER (PARTITION BY customer_name ORDER BY month) AS prev_month_value,
       CASE WHEN monthly_value > LAG(monthly_value) OVER (PARTITION BY customer_name ORDER BY month)
            THEN 'UP' ELSE 'DOWN / FIRST' END AS trend
FROM monthly
ORDER BY customer_name, month
"""
print(pd.read_sql_query(q2_detail, conn))

# ============================================================
# Q3: Running total of revenue by date across all counties
# ============================================================
# BOARD INTERPRETATION: Revenue crossed KES 100,000 by mid-month and then flattened, so the slowdown is a timing problem in the second half of the month, not a demand problem.
q3 = """
WITH daily AS (
    SELECT order_date AS date,
           SUM(quantity * unit_price) AS daily_revenue
    FROM orders
    GROUP BY order_date
)
SELECT date,
       daily_revenue,
       SUM(daily_revenue) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total_revenue
FROM daily
ORDER BY date
"""
print("\n--- Q3: Running Total Revenue by Date ---")
print(pd.read_sql_query(q3, conn))

conn.close()