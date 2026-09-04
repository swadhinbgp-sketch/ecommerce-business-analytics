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
    ),
    parse_dates=["order_date"]
)


# ============================================================
# YEARLY PERFORMANCE
# ============================================================

yearly = (
    df.groupby("year")
    .agg(
        orders=("order_id", "nunique"),
        customers=("customer_id", "nunique"),
        gross_sales=("gross_sales", "sum"),
        discounts=("discount_amount", "sum"),
        net_sales=("net_sales", "sum"),
        realized_sales=("realized_sales", "sum"),
        realized_profit=("realized_profit", "sum")
    )
    .reset_index()
)


# ============================================================
# CALCULATE METRICS
# ============================================================

yearly["profit_margin"] = (
    yearly["realized_profit"]
    / yearly["realized_sales"]
)


yearly["aov"] = (
    yearly["realized_sales"]
    / yearly["orders"]
)


# Year-over-year growth
yearly["sales_growth"] = (
    yearly["realized_sales"]
    .pct_change()
)


yearly["profit_growth"] = (
    yearly["realized_profit"]
    .pct_change()
)


yearly["order_growth"] = (
    yearly["orders"]
    .pct_change()
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("=" * 80)
print("YEAR-OVER-YEAR BUSINESS PERFORMANCE")
print("=" * 80)

print()

display_columns = [
    "year",
    "orders",
    "customers",
    "realized_sales",
    "realized_profit",
    "profit_margin",
    "aov",
    "sales_growth",
    "profit_growth",
    "order_growth"
]

print(
    yearly[display_columns].to_string(
        index=False,
        formatters={
            "realized_sales": "₹{:,.2f}".format,
            "realized_profit": "₹{:,.2f}".format,
            "profit_margin": "{:.2%}".format,
            "aov": "₹{:,.2f}".format,
            "sales_growth": lambda x: (
                "N/A"
                if pd.isna(x)
                else f"{x:.2%}"
            ),
            "profit_growth": lambda x: (
                "N/A"
                if pd.isna(x)
                else f"{x:.2%}"
            ),
            "order_growth": lambda x: (
                "N/A"
                if pd.isna(x)
                else f"{x:.2%}"
            )
        }
    )
)


# ============================================================
# TREND SUMMARY
# ============================================================

first_year = yearly.iloc[0]
last_year = yearly.iloc[-1]


overall_sales_change = (
    last_year["realized_sales"]
    / first_year["realized_sales"]
    - 1
)


overall_profit_change = (
    last_year["realized_profit"]
    / first_year["realized_profit"]
    - 1
)


overall_order_change = (
    last_year["orders"]
    / first_year["orders"]
    - 1
)


print("\n")
print("=" * 80)
print("3-YEAR TREND SUMMARY")
print("=" * 80)

print(
    f"\nRealized Sales Change: "
    f"{overall_sales_change:.2%}"
)

print(
    f"Profit Change: "
    f"{overall_profit_change:.2%}"
)

print(
    f"Order Volume Change: "
    f"{overall_order_change:.2%}"
)


# ============================================================
# BEST / WORST YEAR
# ============================================================

best_sales_year = yearly.loc[
    yearly["realized_sales"].idxmax(),
    "year"
]

worst_sales_year = yearly.loc[
    yearly["realized_sales"].idxmin(),
    "year"
]

best_profit_year = yearly.loc[
    yearly["realized_profit"].idxmax(),
    "year"
]

worst_profit_year = yearly.loc[
    yearly["realized_profit"].idxmin(),
    "year"
]


print("\nBest Sales Year:", best_sales_year)
print("Worst Sales Year:", worst_sales_year)

print("\nBest Profit Year:", best_profit_year)
print("Worst Profit Year:", worst_profit_year)


print("\n")
print("=" * 80)
print("YEARLY ANALYSIS COMPLETE")
print("=" * 80)