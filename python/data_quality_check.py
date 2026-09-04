import os
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RAW_DIR = os.path.join(
    BASE_DIR,
    "data",
    "raw"
)


# ============================================================
# LOAD DATA
# ============================================================

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
# CUSTOMER INVESTIGATION
# ============================================================

print("=" * 70)
print("CUSTOMER DATA QUALITY CHECK")
print("=" * 70)

print("\nUnique customer IDs:")
print(customers["customer_id"].nunique())

print("\nDuplicate customer IDs:")
print(
    customers["customer_id"].duplicated().sum()
)

print("\nMissing ages:")
print(
    customers["age"].isna().sum()
)

print("\nAge outside valid range:")
print(
    ((customers["age"] < 18) | (customers["age"] > 100)).sum()
)

print("\nGender values:")
print(
    customers["gender"].value_counts()
)

print("\nState values:")
print(
    customers["state"].value_counts()
)

print("\nSignup date range:")
print(
    customers["signup_date"].min(),
    "to",
    customers["signup_date"].max()
)


# ============================================================
# PRODUCT INVESTIGATION
# ============================================================

print("\n")
print("=" * 70)
print("PRODUCT DATA QUALITY CHECK")
print("=" * 70)

print("\nUnique product IDs:")
print(products["product_id"].nunique())

print("\nCategory values:")
print(
    products["category"].value_counts()
)

print("\nSubcategory values:")
print(
    products["subcategory"].value_counts()
)

print("\nProducts where selling price <= cost price:")
print(
    (products["selling_price"] <= products["cost_price"]).sum()
)

print("\nMinimum selling price:")
print(
    products["selling_price"].min()
)

print("\nMaximum selling price:")
print(
    products["selling_price"].max()
)


# ============================================================
# ORDER INVESTIGATION
# ============================================================

print("\n")
print("=" * 70)
print("ORDER DATA QUALITY CHECK")
print("=" * 70)

print("\nUnique order IDs:")
print(orders["order_id"].nunique())

print("\nDuplicate order IDs:")
print(
    orders["order_id"].duplicated().sum()
)

print("\nQuantity <= 0:")
print(
    (orders["quantity"] <= 0).sum()
)

print("\nDiscount outside 0-25%:")
print(
    ((orders["discount"] < 0) | (orders["discount"] > 0.25)).sum()
)

print("\nMissing shipping costs:")
print(
    orders["shipping_cost"].isna().sum()
)

print("\nPayment methods:")
print(
    orders["payment_method"].value_counts()
)

print("\nOrder statuses:")
print(
    orders["order_status"].value_counts()
)

print("\nRegions:")
print(
    orders["region"].value_counts()
)

print("\nOrder date range:")
print(
    orders["order_date"].min(),
    "to",
    orders["order_date"].max()
)


# ============================================================
# REFERENTIAL INTEGRITY
# ============================================================

print("\n")
print("=" * 70)
print("REFERENTIAL INTEGRITY CHECK")
print("=" * 70)

customer_ids = set(customers["customer_id"])
product_ids = set(products["product_id"])

invalid_customers = (
    ~orders["customer_id"].isin(customer_ids)
).sum()

invalid_products = (
    ~orders["product_id"].isin(product_ids)
).sum()

print("\nOrders with invalid customer IDs:")
print(invalid_customers)

print("\nOrders with invalid product IDs:")
print(invalid_products)


# ============================================================
# SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("DATA QUALITY CHECK COMPLETE")
print("=" * 70)