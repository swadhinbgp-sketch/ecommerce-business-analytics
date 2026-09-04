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

products = pd.read_csv(
    os.path.join(
        CLEAN_DIR,
        "products_clean.csv"
    )
)

master = pd.read_csv(
    os.path.join(
        CLEAN_DIR,
        "sales_master.csv"
    )
)


# ============================================================
# PRODUCT MASTER MAPPING
# ============================================================

print("=" * 90)
print("PRODUCT MASTER — CATEGORY / SUBCATEGORY MAPPING")
print("=" * 90)

mapping = (
    products
    .groupby("category")["subcategory"]
    .unique()
)

for category, subcategories in mapping.items():
    print(f"\n{category}:")
    print(", ".join(sorted(subcategories)))


# ============================================================
# CHECK ELECTRONICS SPECIFICALLY
# ============================================================

print("\n")
print("=" * 90)
print("ELECTRONICS PRODUCTS — SUBCATEGORY CHECK")
print("=" * 90)

electronics_products = products[
    products["category"] == "Electronics"
]

print(
    electronics_products[
        [
            "product_id",
            "product_name",
            "category",
            "subcategory"
        ]
    ].to_string(index=False)
)


# ============================================================
# MASTER DATASET MAPPING
# ============================================================

print("\n")
print("=" * 90)
print("MASTER DATASET — ELECTRONICS SUBCATEGORY CHECK")
print("=" * 90)

electronics_master = master[
    master["category"] == "Electronics"
]

master_mapping = (
    electronics_master
    .groupby("subcategory")
    .agg(
        rows=("order_id", "count"),
        products=("product_id", "nunique"),
        sales=("realized_sales", "sum")
    )
    .reset_index()
    .sort_values("sales", ascending=False)
)

print(
    master_mapping.to_string(
        index=False,
        formatters={
            "sales": "₹{:,.2f}".format
        }
    )
)


# ============================================================
# CHECK CATEGORY-SUBCATEGORY COMBINATIONS
# ============================================================

print("\n")
print("=" * 90)
print("ALL CATEGORY / SUBCATEGORY COMBINATIONS")
print("=" * 90)

combinations = (
    products[
        ["category", "subcategory"]
    ]
    .drop_duplicates()
    .sort_values(
        ["category", "subcategory"]
    )
)

print(
    combinations.to_string(index=False)
)


# ============================================================
# SUMMARY
# ============================================================

print("\n")
print("=" * 90)
print("PRODUCT MAPPING DIAGNOSTIC COMPLETE")
print("=" * 90)