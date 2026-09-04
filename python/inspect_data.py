import os
import pandas as pd


# Project directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")


# Load datasets
customers = pd.read_csv(
    os.path.join(RAW_DIR, "customers.csv")
)

products = pd.read_csv(
    os.path.join(RAW_DIR, "products.csv")
)

orders = pd.read_csv(
    os.path.join(RAW_DIR, "orders.csv")
)


# ============================================================
# CUSTOMERS
# ============================================================

print("=" * 70)
print("CUSTOMERS DATASET")
print("=" * 70)

print("\nShape:")
print(customers.shape)

print("\nColumns:")
print(customers.columns.tolist())

print("\nData Types:")
print(customers.dtypes)

print("\nMissing Values:")
print(customers.isnull().sum())

print("\nDuplicate Rows:")
print(customers.duplicated().sum())

print("\nFirst 5 Rows:")
print(customers.head())


# ============================================================
# PRODUCTS
# ============================================================

print("\n")
print("=" * 70)
print("PRODUCTS DATASET")
print("=" * 70)

print("\nShape:")
print(products.shape)

print("\nColumns:")
print(products.columns.tolist())

print("\nData Types:")
print(products.dtypes)

print("\nMissing Values:")
print(products.isnull().sum())

print("\nDuplicate Rows:")
print(products.duplicated().sum())

print("\nFirst 5 Rows:")
print(products.head())


# ============================================================
# ORDERS
# ============================================================

print("\n")
print("=" * 70)
print("ORDERS DATASET")
print("=" * 70)

print("\nShape:")
print(orders.shape)

print("\nColumns:")
print(orders.columns.tolist())

print("\nData Types:")
print(orders.dtypes)

print("\nMissing Values:")
print(orders.isnull().sum())

print("\nDuplicate Rows:")
print(orders.duplicated().sum())

print("\nFirst 5 Rows:")
print(orders.head())


# ============================================================
# BASIC STATISTICS
# ============================================================

print("\n")
print("=" * 70)
print("NUMERICAL SUMMARY")
print("=" * 70)

print("\nCustomers:")
print(customers.describe())

print("\nProducts:")
print(products.describe())

print("\nOrders:")
print(orders.describe())