import sqlite3
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CLEANED_DIR = DATA_DIR / "cleaned"
DB_PATH = DATA_DIR / "ecommerce.db"

# Load cleaned CSV files
customers = pd.read_csv(CLEANED_DIR / "customers_clean.csv")
products = pd.read_csv(CLEANED_DIR / "products_clean.csv")
orders = pd.read_csv(CLEANED_DIR / "orders_clean.csv")

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)

# Load data into SQLite tables
customers.to_sql("customers", conn, if_exists="replace", index=False)
products.to_sql("products", conn, if_exists="replace", index=False)
orders.to_sql("orders", conn, if_exists="replace", index=False)

# Create indexes for better query performance
conn.execute("""
    CREATE INDEX IF NOT EXISTS idx_orders_customer_id
    ON orders(customer_id)
""")

conn.execute("""
    CREATE INDEX IF NOT EXISTS idx_orders_product_id
    ON orders(product_id)
""")

conn.execute("""
    CREATE INDEX IF NOT EXISTS idx_orders_order_date
    ON orders(order_date)
""")

conn.commit()

# Verify row counts
print("SQLite database loaded successfully.")
print(f"Customers: {len(customers):,}")
print(f"Products: {len(products):,}")
print(f"Orders: {len(orders):,}")

conn.close()