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
    os.path.join(
        CLEAN_DIR,
        "customers_clean.csv"
    ),
    parse_dates=["signup_date"]
)

products = pd.read_csv(
    os.path.join(
        CLEAN_DIR,
        "products_clean.csv"
    )
)

orders = pd.read_csv(
    os.path.join(
        CLEAN_DIR,
        "orders_clean.csv"
    ),
    parse_dates=["order_date"]
)


print("=" * 70)
print("BUILDING MASTER ANALYTICAL DATASET")
print("=" * 70)


# ============================================================
# MERGE ORDERS WITH CUSTOMERS
# ============================================================

master = orders.merge(
    customers,
    on="customer_id",
    how="left",
    validate="many_to_one"
)


# ============================================================
# MERGE WITH PRODUCTS
# ============================================================

master = master.merge(
    products,
    on="product_id",
    how="left",
    validate="many_to_one"
)


# ============================================================
# CALCULATE BUSINESS METRICS
# ============================================================

# Gross sales before discount
master["gross_sales"] = (
    master["selling_price"]
    * master["quantity"]
)


# Discount amount
master["discount_amount"] = (
    master["gross_sales"]
    * master["discount"]
)


# Net sales after discount
master["net_sales"] = (
    master["gross_sales"]
    - master["discount_amount"]
)


# Product cost
master["product_cost"] = (
    master["cost_price"]
    * master["quantity"]
)


# Profit before shipping
master["profit_before_shipping"] = (
    master["net_sales"]
    - master["product_cost"]
)


# Profit after shipping
master["profit"] = (
    master["profit_before_shipping"]
    - master["shipping_cost"]
)


# Profit margin
master["profit_margin"] = (
    master["profit"]
    / master["net_sales"]
)

# ============================================================
# BUSINESS STATUS METRICS
# ============================================================

master["is_delivered"] = (
    master["order_status"] == "Delivered"
).astype(int)

master["is_returned"] = (
    master["order_status"] == "Returned"
).astype(int)

master["is_cancelled"] = (
    master["order_status"] == "Cancelled"
).astype(int)


# Realized sales only from delivered orders
master["realized_sales"] = (
    master["net_sales"]
    .where(
        master["order_status"] == "Delivered",
        0
    )
)


# Realized profit only from delivered orders
master["realized_profit"] = (
    master["profit"]
    .where(
        master["order_status"] == "Delivered",
        0
    )
)
# ============================================================
# ADD TIME DIMENSIONS
# ============================================================

master["year"] = (
    master["order_date"].dt.year
)

master["month"] = (
    master["order_date"].dt.month
)

master["month_name"] = (
    master["order_date"].dt.month_name()
)

master["quarter"] = (
    "Q"
    + master["order_date"]
    .dt.quarter
    .astype(str)
)

master["year_month"] = (
    master["order_date"]
    .dt.to_period("M")
    .astype(str)
)


# ============================================================
# CUSTOMER AGE GROUP
# ============================================================

master["age_group"] = pd.cut(
    master["age"],
    bins=[17, 25, 35, 45, 55, 100],
    labels=[
        "18-25",
        "26-35",
        "36-45",
        "46-55",
        "56+"
    ]
)


# ============================================================
# SAVE MASTER DATASET
# ============================================================

output_path = os.path.join(
    CLEAN_DIR,
    "sales_master.csv"
)

master.to_csv(
    output_path,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print("\nMaster dataset created successfully.")

print("\nRows:", len(master))

print("Columns:", len(master.columns))

print("\nOutput file:")
print(output_path)

print("\nBusiness metrics:")
print(
    [
        "gross_sales",
        "discount_amount",
        "net_sales",
        "product_cost",
        "profit_before_shipping",
        "profit",
        "profit_margin",
        "realized_sales",
        "realized_profit",
        "is_delivered",
        "is_returned",
        "is_cancelled"
    ]
)

print("\nTime dimensions:")
print(
    [
        "year",
        "month",
        "month_name",
        "quarter",
        "year_month"
    ]
)

print("\nCustomer dimension:")
print("age_group")

print("\nFirst 5 rows:")
print(master.head())

print("\n" + "=" * 70)
print("MASTER DATASET COMPLETE")
print("=" * 70)