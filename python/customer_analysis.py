import os
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MASTER_PATH = os.path.join(
    BASE_DIR,
    "data",
    "cleaned",
    "sales_master.csv"
)


# ============================================================
# LOAD MASTER DATASET
# ============================================================

df = pd.read_csv(MASTER_PATH)

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 100)
print("CUSTOMER ANALYTICS")
print("=" * 100)


# ============================================================
# 1. CUSTOMER OVERVIEW
# ============================================================

customer_summary = (
    df.groupby("customer_id")
    .agg(
        orders=("order_id", "nunique"),
        quantity=("quantity", "sum"),
        realized_sales=("realized_sales", "sum"),
        realized_profit=("realized_profit", "sum")
    )
    .reset_index()
)


customer_summary["profit_margin"] = (
    customer_summary["realized_profit"]
    / customer_summary["realized_sales"]
    * 100
)


print("\n")
print("=" * 100)
print("CUSTOMER OVERVIEW")
print("=" * 100)

print(
    f"Total Customers: "
    f"{customer_summary['customer_id'].nunique():,}"
)

print(
    f"Average Orders per Customer: "
    f"{customer_summary['orders'].mean():.2f}"
)

print(
    f"Average Realized Sales per Customer: "
    f"₹{customer_summary['realized_sales'].mean():,.2f}"
)

print(
    f"Average Realized Profit per Customer: "
    f"₹{customer_summary['realized_profit'].mean():,.2f}"
)


# ============================================================
# 2. REPEAT CUSTOMER ANALYSIS
# ============================================================

repeat_customers = customer_summary[
    customer_summary["orders"] > 1
]

one_time_customers = customer_summary[
    customer_summary["orders"] == 1
]

repeat_customer_rate = (
    len(repeat_customers)
    / len(customer_summary)
    * 100
)


print("\n")
print("=" * 100)
print("REPEAT CUSTOMER ANALYSIS")
print("=" * 100)

print(
    f"One-time Customers: "
    f"{len(one_time_customers):,}"
)

print(
    f"Repeat Customers: "
    f"{len(repeat_customers):,}"
)

print(
    f"Repeat Customer Rate: "
    f"{repeat_customer_rate:.2f}%"
)


# ============================================================
# 3. TOP 10 CUSTOMERS BY REALIZED SALES
# ============================================================

top_customers = (
    customer_summary
    .sort_values(
        "realized_sales",
        ascending=False
    )
    .head(10)
)


print("\n")
print("=" * 100)
print("TOP 10 CUSTOMERS BY REALIZED SALES")
print("=" * 100)

print(
    top_customers[
        [
            "customer_id",
            "orders",
            "quantity",
            "realized_sales",
            "realized_profit",
            "profit_margin"
        ]
    ].to_string(
        index=False,
        formatters={
            "realized_sales": "₹{:,.2f}".format,
            "realized_profit": "₹{:,.2f}".format,
            "profit_margin": "{:.2f}%".format
        }
    )
)


# ============================================================
# 4. TOP 10 CUSTOMERS BY PROFIT
# ============================================================

top_profit_customers = (
    customer_summary
    .sort_values(
        "realized_profit",
        ascending=False
    )
    .head(10)
)


print("\n")
print("=" * 100)
print("TOP 10 CUSTOMERS BY REALIZED PROFIT")
print("=" * 100)

print(
    top_profit_customers[
        [
            "customer_id",
            "orders",
            "quantity",
            "realized_sales",
            "realized_profit",
            "profit_margin"
        ]
    ].to_string(
        index=False,
        formatters={
            "realized_sales": "₹{:,.2f}".format,
            "realized_profit": "₹{:,.2f}".format,
            "profit_margin": "{:.2f}%".format
        }
    )
)


# ============================================================
# 5. AGE GROUP ANALYSIS
# ============================================================

age_analysis = (
    df.groupby("age_group")
    .agg(
        customers=("customer_id", "nunique"),
        orders=("order_id", "nunique"),
        quantity=("quantity", "sum"),
        realized_sales=("realized_sales", "sum"),
        realized_profit=("realized_profit", "sum")
    )
    .reset_index()
)


age_analysis["profit_margin"] = (
    age_analysis["realized_profit"]
    / age_analysis["realized_sales"]
    * 100
)

age_analysis["sales_per_customer"] = (
    age_analysis["realized_sales"]
    / age_analysis["customers"]
)


print("\n")
print("=" * 100)
print("AGE GROUP PERFORMANCE")
print("=" * 100)

print(
    age_analysis.to_string(
        index=False,
        formatters={
            "realized_sales": "₹{:,.2f}".format,
            "realized_profit": "₹{:,.2f}".format,
            "profit_margin": "{:.2f}%".format,
            "sales_per_customer": "₹{:,.2f}".format
        }
    )
)


# ============================================================
# 6. CUSTOMER VALUE SEGMENTS
# ============================================================

customer_summary["customer_segment"] = pd.cut(
    customer_summary["realized_sales"],
    bins=[
        -float("inf"),
        10000,
        25000,
        50000,
        100000,
        float("inf")
    ],
    labels=[
        "Low Value",
        "Medium Value",
        "High Value",
        "Very High Value",
        "VIP"
    ]
)


segment_analysis = (
    customer_summary
    .groupby(
        "customer_segment",
        observed=True
    )
    .agg(
        customers=("customer_id", "count"),
        orders=("orders", "sum"),
        realized_sales=("realized_sales", "sum"),
        realized_profit=("realized_profit", "sum")
    )
    .reset_index()
)


segment_analysis["sales_share"] = (
    segment_analysis["realized_sales"]
    / customer_summary["realized_sales"].sum()
    * 100
)


print("\n")
print("=" * 100)
print("CUSTOMER VALUE SEGMENTS")
print("=" * 100)

print(
    segment_analysis.to_string(
        index=False,
        formatters={
            "realized_sales": "₹{:,.2f}".format,
            "realized_profit": "₹{:,.2f}".format,
            "sales_share": "{:.2f}%".format
        }
    )
)


# ============================================================
# 7. TOP AGE GROUP BY SALES
# ============================================================

best_age_group = age_analysis.loc[
    age_analysis["realized_sales"].idxmax(),
    "age_group"
]


# ============================================================
# 8. TOP CUSTOMER
# ============================================================

best_customer = top_customers.iloc[0]


# ============================================================
# 9. BUSINESS INSIGHTS
# ============================================================

print("\n")
print("=" * 100)
print("KEY CUSTOMER INSIGHTS")
print("=" * 100)

print(
    f"Highest-value customer by sales: "
    f"{best_customer['customer_id']}"
)

print(
    f"Customer sales from this customer: "
    f"₹{best_customer['realized_sales']:,.2f}"
)

print(
    f"Best-performing age group by realized sales: "
    f"{best_age_group}"
)

print(
    f"Repeat customer rate: "
    f"{repeat_customer_rate:.2f}%"
)


print("\n")
print("=" * 100)
print("CUSTOMER ANALYSIS COMPLETE")
print("=" * 100)