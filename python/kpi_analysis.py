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
# LOAD MASTER DATA
# ============================================================

df = pd.read_csv(
    os.path.join(
        CLEAN_DIR,
        "sales_master.csv"
    ),
    parse_dates=["order_date", "signup_date"]
)


# ============================================================
# BASIC KPIs
# ============================================================

total_orders = df["order_id"].nunique()

total_customers = df["customer_id"].nunique()

total_products = df["product_id"].nunique()

gross_sales = df["gross_sales"].sum()

total_discount = df["discount_amount"].sum()

net_sales = df["net_sales"].sum()

realized_sales = df["realized_sales"].sum()

total_profit = df["realized_profit"].sum()


# ============================================================
# PROFIT MARGIN
# ============================================================

realized_profit_margin = (
    total_profit / realized_sales
    if realized_sales != 0
    else 0
)


# ============================================================
# AVERAGE ORDER VALUE
# ============================================================

aov = (
    realized_sales / total_orders
    if total_orders != 0
    else 0
)


# ============================================================
# ORDER STATUS METRICS
# ============================================================

delivered_orders = (
    df["is_delivered"].sum()
)

returned_orders = (
    df["is_returned"].sum()
)

cancelled_orders = (
    df["is_cancelled"].sum()
)


return_rate = (
    returned_orders / total_orders
    if total_orders != 0
    else 0
)

cancellation_rate = (
    cancelled_orders / total_orders
    if total_orders != 0
    else 0
)

delivery_rate = (
    delivered_orders / total_orders
    if total_orders != 0
    else 0
)


# ============================================================
# CUSTOMER METRICS
# ============================================================

orders_per_customer = (
    total_orders / total_customers
    if total_customers != 0
    else 0
)


# Customers with more than one order
customer_order_counts = (
    df.groupby("customer_id")["order_id"]
    .nunique()
)

repeat_customers = (
    (customer_order_counts > 1).sum()
)

repeat_customer_rate = (
    repeat_customers / total_customers
    if total_customers != 0
    else 0
)


# ============================================================
# PRINT EXECUTIVE SUMMARY
# ============================================================

print("=" * 70)
print("E-COMMERCE BUSINESS — EXECUTIVE KPI SUMMARY")
print("=" * 70)

print(f"\nTotal Orders:              {total_orders:,}")

print(f"Total Customers:           {total_customers:,}")

print(f"Total Products:            {total_products:,}")

print(f"Gross Sales:               ₹{gross_sales:,.2f}")

print(f"Total Discounts:           ₹{total_discount:,.2f}")

print(f"Net Sales:                 ₹{net_sales:,.2f}")

print(f"Realized Sales:            ₹{realized_sales:,.2f}")

print(f"Realized Profit:           ₹{total_profit:,.2f}")

print(
    f"Realized Profit Margin:    "
    f"{realized_profit_margin:.2%}"
)

print(f"Average Order Value:       ₹{aov:,.2f}")


print("\nORDER PERFORMANCE")
print("-" * 70)

print(
    f"Delivered Orders:          "
    f"{delivered_orders:,}"
)

print(
    f"Returned Orders:           "
    f"{returned_orders:,}"
)

print(
    f"Cancelled Orders:          "
    f"{cancelled_orders:,}"
)

print(
    f"Delivery Rate:             "
    f"{delivery_rate:.2%}"
)

print(
    f"Return Rate:               "
    f"{return_rate:.2%}"
)

print(
    f"Cancellation Rate:         "
    f"{cancellation_rate:.2%}"
)


print("\nCUSTOMER PERFORMANCE")
print("-" * 70)

print(
    f"Orders per Customer:       "
    f"{orders_per_customer:.2f}"
)

print(
    f"Repeat Customers:          "
    f"{repeat_customers:,}"
)

print(
    f"Repeat Customer Rate:      "
    f"{repeat_customer_rate:.2%}"
)


# ============================================================
# YEARLY PERFORMANCE
# ============================================================

print("\nYEARLY PERFORMANCE")
print("-" * 70)

yearly = (
    df.groupby("year")
    .agg(
        orders=("order_id", "nunique"),
        customers=("customer_id", "nunique"),
        realized_sales=("realized_sales", "sum"),
        realized_profit=("realized_profit", "sum")
    )
    .reset_index()
)

yearly["profit_margin"] = (
    yearly["realized_profit"]
    / yearly["realized_sales"]
)

print(yearly.to_string(index=False))


print("\n")
print("=" * 70)
print("KPI ANALYSIS COMPLETE")
print("=" * 70)