import sqlite3
import pandas as pd

DB = "distributor.db"

def get_county_report(county, start_date, end_date):
    """
    Returns a clean summary for Monday report.
    county: e.g. "Mombasa"
    start_date, end_date: "YYYY-MM-DD" e.g. "2024-01-01"
    """
    conn = sqlite3.connect(DB)

    # Parameterized - 3 x ? placeholders, NEVER f-string
    query = """
        SELECT o.product AS product,
               COUNT(*) AS total_orders,
               SUM(o.quantity) AS total_quantity,
               SUM(o.quantity * o.unit_price) AS total_revenue_kes
        FROM orders o
        JOIN customers c ON c.customer = o.customer_name
        WHERE c.county = ?
          AND o.order_date >= ?
          AND o.order_date <= ?
        GROUP BY o.product
        ORDER BY total_revenue_kes DESC
    """

    try:
        df = pd.read_sql_query(
            query, conn,
            params=(county, start_date, end_date)
        )
    except sqlite3.OperationalError as e:
        print(f"ERROR: {e}")
        print("Check your column names with: PRAGMA table_info(orders);")
        conn.close()
        return pd.DataFrame()

    conn.close()

    # Handle no results
    if df.empty:
        print(f"No orders found for {county} between {start_date} and {end_date}.")
        return df

    return df

if __name__ == "__main__":
    # TEST 1: Mombasa - your biggest county
    print("\n--- TEST 1: Mombasa, all time ---")
    print(get_county_report("Mombasa", "2020-01-01", "2026-12-31"))

    # TEST 2: Kisumu
    print("\n--- TEST 2: Kisumu, all time ---")
    print(get_county_report("Kisumu", "2020-01-01", "2026-12-31"))

    # TEST 3: Nairobi
    print("\n--- TEST 3: Nairobi, all time ---")
    print(get_county_report("Nairobi", "2020-01-01", "2026-12-31"))

    # TEST 4: No results case
    print("\n--- TEST 4: No results - fake county ---")
    print(get_county_report("Mars", "2020-01-01", "2026-12-31"))

    # TEST 5: Hacker test - should return empty, not everything
    print("\n--- TEST 5: Hacker test ---")
    print(get_county_report("' OR 1=1 --", "2020-01-01", "2026-12-31"))