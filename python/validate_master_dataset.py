import os
import pandas as pd


# ============================================================
# PROJECT PATH
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
# LOAD MASTER DATASET
# ============================================================

master = pd.read_csv(
    os.path.join(
        CLEAN_DIR,
        "sales_master.csv"
    ),
    parse_dates=["order_date", "signup_date"]
)


print("=" * 70)
print("MASTER DATASET VALIDATION")
print("=" * 70)


# ============================================================
# BASIC CHECKS
# ============================================================

print("\nBASIC INFORMATION")
print("-" * 70)

print("Rows:", len(master))
print("Columns:", len(master.columns))

print(
    "Duplicate order IDs:",
    master["order_id"].duplicated().sum()
)

print(
    "Missing values:",
    master.isnull().sum().sum()
)


# ============================================================
# BUSINESS METRIC CHECKS
# ============================================================

print("\nBUSINESS METRICS")
print("-" * 70)

print(
    "Negative net sales:",
    (master["net_sales"] < 0).sum()
)

print(
    "Negative product cost:",
    (master["product_cost"] < 0).sum()
)

print(
    "Delivered orders:",
    master["is_delivered"].sum()
)

print(
    "Returned orders:",
    master["is_returned"].sum()
)

print(
    "Cancelled orders:",
    master["is_cancelled"].sum()
)


# ============================================================
# STATUS LOGIC CHECK
# ============================================================

print("\nSTATUS LOGIC")
print("-" * 70)

print(
    "Delivered rows with realized_sales = 0:",
    (
        (master["order_status"] == "Delivered")
        & (master["realized_sales"] == 0)
    ).sum()
)

print(
    "Non-delivered rows with realized_sales > 0:",
    (
        (master["order_status"] != "Delivered")
        & (master["realized_sales"] > 0)
    ).sum()
)

print(
    "Delivered rows with realized_profit = 0:",
    (
        (master["order_status"] == "Delivered")
        & (master["realized_profit"] == 0)
    ).sum()
)


# ============================================================
# PROFIT MARGIN CHECK
# ============================================================

print("\nPROFIT MARGIN")
print("-" * 70)

print(
    "Infinite profit margins:",
    (~master["profit_margin"].abs().lt(float("inf"))).sum()
)

print(
    "Profit margin below -100%:",
    (master["profit_margin"] < -1).sum()
)


# ============================================================
# CUSTOMER / PRODUCT COVERAGE
# ============================================================

print("\nCUSTOMER & PRODUCT COVERAGE")
print("-" * 70)

print(
    "Unique customers:",
    master["customer_id"].nunique()
)

print(
    "Unique products:",
    master["product_id"].nunique()
)

print(
    "Unique categories:",
    master["category"].nunique()
)

print(
    "Unique cities:",
    master["city"].nunique()
)


# ============================================================
# DATE COVERAGE
# ============================================================

print("\nDATE COVERAGE")
print("-" * 70)

print(
    "Minimum order date:",
    master["order_date"].min().date()
)

print(
    "Maximum order date:",
    master["order_date"].max().date()
)


# ============================================================
# STATUS SUMMARY
# ============================================================

print("\nORDER STATUS SUMMARY")
print("-" * 70)

print(
    master["order_status"].value_counts()
)


# ============================================================
# FINAL CHECK
# ============================================================

checks = [
    len(master) == 59980,
    master["order_id"].duplicated().sum() == 0,
    master.isnull().sum().sum() == 0,
    (master["net_sales"] < 0).sum() == 0,
    (master["product_cost"] < 0).sum() == 0,
    (
        (
            (master["order_status"] == "Delivered")
            & (master["realized_sales"] == 0)
        ).sum()
        == 0
    ),
    (
        (
            (master["order_status"] != "Delivered")
            & (master["realized_sales"] > 0)
        ).sum()
        == 0
    )
]


print("\n")
print("=" * 70)

if all(checks):
    print("RESULT: PASS")
    print("Master dataset passed validation.")
else:
    print("RESULT: REVIEW REQUIRED")
    print("One or more checks failed.")

print("=" * 70)