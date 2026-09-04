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
# FILTER ELECTRONICS
# ============================================================

electronics = df[
    df["category"] == "Electronics"
].copy()


# ============================================================
# YEARLY PERFORMANCE
# ============================================================

yearly = (
    electronics
    .groupby("year")
    .agg(
        orders=("order_id", "nunique"),
        quantity=("quantity", "sum"),
        realized_sales=("realized_sales", "sum"),
        realized_profit=("realized_profit", "sum"),
        discounts=("discount_amount", "sum"),
        shipping_cost=("shipping_cost", "sum")
    )
    .reset_index()
)


yearly["aov"] = (
    yearly["realized_sales"]
    / yearly["orders"]
)


yearly["profit_margin"] = (
    yearly["realized_profit"]
    / yearly["realized_sales"]
)


yearly["sales_per_unit"] = (
    yearly["realized_sales"]
    / yearly["quantity"]
)


# ============================================================
# DISPLAY YEARLY PERFORMANCE
# ============================================================

print("=" * 100)
print("ELECTRONICS — YEARLY PERFORMANCE")
print("=" * 100)

print(
    yearly.to_string(
        index=False,
        formatters={
            "realized_sales": "₹{:,.2f}".format,
            "realized_profit": "₹{:,.2f}".format,
            "discounts": "₹{:,.2f}".format,
            "shipping_cost": "₹{:,.2f}".format,
            "aov": "₹{:,.2f}".format,
            "profit_margin": "{:.2%}".format,
            "sales_per_unit": "₹{:,.2f}".format
        }
    )
)


# ============================================================
# ELECTRONICS SUBCATEGORY
# ============================================================

subcategory = (
    electronics
    .groupby("subcategory")
    .agg(
        orders=("order_id", "nunique"),
        quantity=("quantity", "sum"),
        realized_sales=("realized_sales", "sum"),
        realized_profit=("realized_profit", "sum")
    )
    .reset_index()
)


subcategory["profit_margin"] = (
    subcategory["realized_profit"]
    / subcategory["realized_sales"]
)


subcategory["sales_share"] = (
    subcategory["realized_sales"]
    / subcategory["realized_sales"].sum()
)


subcategory = subcategory.sort_values(
    "realized_sales",
    ascending=False
)


print("\n")
print("=" * 100)
print("ELECTRONICS SUBCATEGORY PERFORMANCE")
print("=" * 100)

print(
    subcategory.to_string(
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
# TOP ELECTRONICS PRODUCTS
# ============================================================

products = (
    electronics
    .groupby(
        [
            "product_id",
            "product_name",
            "subcategory"
        ]
    )
    .agg(
        orders=("order_id", "nunique"),
        quantity=("quantity", "sum"),
        realized_sales=("realized_sales", "sum"),
        realized_profit=("realized_profit", "sum")
    )
    .reset_index()
)


products["profit_margin"] = (
    products["realized_profit"]
    / products["realized_sales"]
)


top_products = products.sort_values(
    "realized_sales",
    ascending=False
).head(15)


print("\n")
print("=" * 100)
print("TOP 15 ELECTRONICS PRODUCTS BY REALIZED SALES")
print("=" * 100)

print(
    top_products.to_string(
        index=False,
        formatters={
            "realized_sales": "₹{:,.2f}".format,
            "realized_profit": "₹{:,.2f}".format,
            "profit_margin": "{:.2%}".format
        }
    )
)


# ============================================================
# WORST PRODUCTS BY PROFIT
# ============================================================

worst_products = products.sort_values(
    "realized_profit"
).head(10)


print("\n")
print("=" * 100)
print("BOTTOM 10 ELECTRONICS PRODUCTS BY PROFIT")
print("=" * 100)

print(
    worst_products.to_string(
        index=False,
        formatters={
            "realized_sales": "₹{:,.2f}".format,
            "realized_profit": "₹{:,.2f}".format,
            "profit_margin": "{:.2%}".format
        }
    )
)


print("\n")
print("=" * 100)
print("ELECTRONICS ANALYSIS COMPLETE")
print("=" * 100)