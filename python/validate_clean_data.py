import os
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

CLEAN_DIR = os.path.join(
    BASE_DIR,
    "data",
    "cleaned"
)


# ============================================================
# LOAD CLEAN DATA
# ============================================================

customers = pd.read_csv(
    os.path.join(CLEAN_DIR, "customers_clean.csv"),
    parse_dates=["signup_date"]
)

products = pd.read_csv(
    os.path.join(CLEAN_DIR, "products_clean.csv")
)

orders = pd.read_csv(
    os.path.join(CLEAN_DIR, "orders_clean.csv"),
    parse_dates=["order_date"]
)


# ============================================================
# VALIDATION HEADER
# ============================================================

print("=" * 70)
print("POST-CLEANING VALIDATION")
print("=" * 70)


# ============================================================
# CUSTOMERS
# ============================================================

print("\nCUSTOMERS")
print("-" * 70)

print("Rows:", len(customers))

print(
    "Duplicate customer IDs:",
    customers["customer_id"].duplicated().sum()
)

print(
    "Missing values:",
    customers.isnull().sum().sum()
)

print(
    "Invalid ages:",
    ((customers["age"] < 18) | (customers["age"] > 100)).sum()
)

print(
    "Date type:",
    customers["signup_date"].dtype
)


# ============================================================
# PRODUCTS
# ============================================================

print("\nPRODUCTS")
print("-" * 70)

print("Rows:", len(products))

print(
    "Duplicate product IDs:",
    products["product_id"].duplicated().sum()
)

print(
    "Missing values:",
    products.isnull().sum().sum()
)

print(
    "Invalid pricing:",
    (
        products["selling_price"]
        <= products["cost_price"]
    ).sum()
)

print("\nCategories:")
print(products["category"].value_counts())


# ============================================================
# ORDERS
# ============================================================

print("\nORDERS")
print("-" * 70)

print("Rows:", len(orders))

print(
    "Duplicate order IDs:",
    orders["order_id"].duplicated().sum()
)

print(
    "Missing values:",
    orders.isnull().sum().sum()
)

print(
    "Invalid quantities:",
    (orders["quantity"] <= 0).sum()
)

print(
    "Invalid discounts:",
    (
        (orders["discount"] < 0)
        | (orders["discount"] > 0.25)
    ).sum()
)

print(
    "Date type:",
    orders["order_date"].dtype
)


# ============================================================
# REFERENTIAL INTEGRITY
# ============================================================

customer_ids = set(
    customers["customer_id"]
)

product_ids = set(
    products["product_id"]
)

invalid_customer_ids = (
    ~orders["customer_id"].isin(customer_ids)
).sum()

invalid_product_ids = (
    ~orders["product_id"].isin(product_ids)
).sum()


print("\nREFERENTIAL INTEGRITY")
print("-" * 70)

print(
    "Invalid customer IDs:",
    invalid_customer_ids
)

print(
    "Invalid product IDs:",
    invalid_product_ids
)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n")
print("=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)

checks = [
    customers["customer_id"].duplicated().sum() == 0,
    customers.isnull().sum().sum() == 0,
    products["product_id"].duplicated().sum() == 0,
    products.isnull().sum().sum() == 0,
    (
        products["selling_price"]
        <= products["cost_price"]
    ).sum() == 0,
    orders["order_id"].duplicated().sum() == 0,
    orders.isnull().sum().sum() == 0,
    (orders["quantity"] <= 0).sum() == 0,
    (
        (orders["discount"] < 0)
        | (orders["discount"] > 0.25)
    ).sum() == 0,
    invalid_customer_ids == 0,
    invalid_product_ids == 0
]

if all(checks):
    print("\nRESULT: PASS")
    print("The cleaned datasets passed all validation checks.")
else:
    print("\nRESULT: REVIEW REQUIRED")
    print("One or more validation checks failed.")

print("=" * 70)