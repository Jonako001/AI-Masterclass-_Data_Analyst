import sqlite3

for db_file in ["distributor.db"]:
    print(f"\n--- {db_file} ---")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Get tables FIRST, save them in a list
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print("Tables:", tables)

    # Now loop over that saved list
    for (table,) in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f" {table}: {count} rows")
    conn.close()