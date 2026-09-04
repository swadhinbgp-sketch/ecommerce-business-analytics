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
# CATEGORY × YEAR
# ============================================================

analysis = (
    df.groupby(["year", "category"])
    .agg(
        orders=("order_id", "nunique"),
        realized_sales=("realized_sales", "sum"),
        realized_profit=("realized_profit", "sum"),
        quantity=("quantity", "sum")
    )
    .reset_index()
)


analysis["profit_margin"] = (
    analysis["realized_profit"]
    / analysis["realized_sales"]
)


# ============================================================
# DISPLAY YEARLY CATEGORY PERFORMANCE
# ============================================================

print("=" * 90)
print("CATEGORY PERFORMANCE BY YEAR")
print("=" * 90)

print(
    analysis.to_string(
        index=False,
        formatters={
            "realized_sales": "₹{:,.2f}".format,
            "realized_profit": "₹{:,.2f}".format,
            "profit_margin": "{:.2%}".format
        }
    )
)


# ============================================================
# 2023 VS 2025 COMPARISON
# ============================================================

comparison = (
    analysis[
        analysis["year"].isin([2023, 2025])
    ]
    .pivot(
        index="category",
        columns="year",
        values=[
            "orders",
            "realized_sales",
            "realized_profit",
            "profit_margin"
        ]
    )
)


# Flatten columns

comparison.columns = [
    f"{metric}_{year}"
    for metric, year in comparison.columns
]


comparison = comparison.reset_index()


# ============================================================
# GROWTH CALCULATIONS
# ============================================================

comparison["sales_change"] = (
    comparison["realized_sales_2025"]
    / comparison["realized_sales_2023"]
    - 1
)


comparison["profit_change"] = (
    comparison["realized_profit_2025"]
    / comparison["realized_profit_2023"]
    - 1
)


comparison["order_change"] = (
    comparison["orders_2025"]
    / comparison["orders_2023"]
    - 1
)


comparison = comparison.sort_values(
    "sales_change"
)


# ============================================================
# DISPLAY COMPARISON
# ============================================================

print("\n")
print("=" * 90)
print("2023 vs 2025 CATEGORY CHANGE")
print("=" * 90)

print(
    comparison[
        [
            "category",
            "sales_change",
            "profit_change",
            "order_change",
            "profit_margin_2023",
            "profit_margin_2025"
        ]
    ].to_string(
        index=False,
        formatters={
            "sales_change": "{:.2%}".format,
            "profit_change": "{:.2%}".format,
            "order_change": "{:.2%}".format,
            "profit_margin_2023": "{:.2%}".format,
            "profit_margin_2025": "{:.2%}".format
        }
    )
)


# ============================================================
# BEST / WORST CATEGORY
# ============================================================

worst_category = comparison.iloc[0]["category"]

best_category = comparison.iloc[-1]["category"]


print("\n")
print("=" * 90)

print(
    "Largest Sales Decline:",
    worst_category
)

print(
    "Strongest Sales Growth:",
    best_category
)

print("=" * 90)
print("CATEGORY YEAR ANALYSIS COMPLETE")
print("=" * 90)