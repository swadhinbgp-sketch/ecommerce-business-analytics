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
# LOAD DATA
# ============================================================

df = pd.read_csv(
    os.path.join(
        CLEAN_DIR,
        "sales_master.csv"
    )
)


# ============================================================
# CATEGORY ANALYSIS
# ============================================================

category = (
    df.groupby("category")
    .agg(
        orders=("order_id", "nunique"),
        customers=("customer_id", "nunique"),
        realized_sales=("realized_sales", "sum"),
        realized_profit=("realized_profit", "sum"),
        quantity=("quantity", "sum")
    )
    .reset_index()
)

category["profit_margin"] = (
    category["realized_profit"]
    / category["realized_sales"]
)

category["sales_share"] = (
    category["realized_sales"]
    / category["realized_sales"].sum()
)


category = category.sort_values(
    "realized_sales",
    ascending=False
)


print("=" * 80)
print("CATEGORY PERFORMANCE")
print("=" * 80)

print(
    category.to_string(
        index=False,
        formatters={
            "realized_sales": "₹{:,.2f}".format,
            "realized_profit": "₹{:,.2f}".format,
            "profit_margin": "{:.2%}".format,
            "sales_share": "{:.2%}".format
        }
    )
)


# ============================================================
# REGION ANALYSIS
# ============================================================

region = (
    df.groupby("region")
    .agg(
        orders=("order_id", "nunique"),
        customers=("customer_id", "nunique"),
        realized_sales=("realized_sales", "sum"),
        realized_profit=("realized_profit", "sum")
    )
    .reset_index()
)

region["profit_margin"] = (
    region["realized_profit"]
    / region["realized_sales"]
)

region["sales_share"] = (
    region["realized_sales"]
    / region["realized_sales"].sum()
)

region = region.sort_values(
    "realized_sales",
    ascending=False
)


print("\n")
print("=" * 80)
print("REGION PERFORMANCE")
print("=" * 80)

print(
    region.to_string(
        index=False,
        formatters={
            "realized_sales": "₹{:,.2f}".format,
            "realized_profit": "₹{:,.2f}".format,
            "profit_margin": "{:.2%}".format,
            "sales_share": "{:.2%}".format
        }
    )
)


# ============================================================
# AGE GROUP ANALYSIS
# ============================================================

age_group = (
    df.groupby("age_group", observed=True)
    .agg(
        orders=("order_id", "nunique"),
        customers=("customer_id", "nunique"),
        realized_sales=("realized_sales", "sum"),
        realized_profit=("realized_profit", "sum")
    )
    .reset_index()
)

age_group["profit_margin"] = (
    age_group["realized_profit"]
    / age_group["realized_sales"]
)

age_group = age_group.sort_values(
    "realized_sales",
    ascending=False
)


print("\n")
print("=" * 80)
print("CUSTOMER AGE GROUP PERFORMANCE")
print("=" * 80)

print(
    age_group.to_string(
        index=False,
        formatters={
            "realized_sales": "₹{:,.2f}".format,
            "realized_profit": "₹{:,.2f}".format,
            "profit_margin": "{:.2%}".format
        }
    )
)


# ============================================================
# PAYMENT METHOD ANALYSIS
# ============================================================

payment = (
    df.groupby("payment_method")
    .agg(
        orders=("order_id", "nunique"),
        realized_sales=("realized_sales", "sum"),
        realized_profit=("realized_profit", "sum")
    )
    .reset_index()
)

payment["profit_margin"] = (
    payment["realized_profit"]
    / payment["realized_sales"]
)

payment = payment.sort_values(
    "realized_sales",
    ascending=False
)


print("\n")
print("=" * 80)
print("PAYMENT METHOD PERFORMANCE")
print("=" * 80)

print(
    payment.to_string(
        index=False,
        formatters={
            "realized_sales": "₹{:,.2f}".format,
            "realized_profit": "₹{:,.2f}".format,
            "profit_margin": "{:.2%}".format
        }
    )
)


print("\n")
print("=" * 80)
print("CATEGORY & REGION ANALYSIS COMPLETE")
print("=" * 80)