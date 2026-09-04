import sqlite3

conn = sqlite3.connect("data/ecommerce.db")

tables = conn.execute(
    "SELECT name FROM sqlite_master WHERE type = 'table'"
).fetchall()

print("Tables:")
for table in tables:
    print("-", table[0])

print("Customers:", conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0])
print("Products:", conn.execute("SELECT COUNT(*) FROM products").fetchone()[0])
print("Orders:", conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0])

conn.close()