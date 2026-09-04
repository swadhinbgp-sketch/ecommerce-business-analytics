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

CLEAN_DIR = os.path.join(
    BASE_DIR,
    "data",
    "cleaned"
)

os.makedirs(CLEAN_DIR, exist_ok=True)


# ============================================================
# LOAD RAW DATA
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


print("=" * 70)
print("STARTING DATA CLEANING")
print("=" * 70)


# ============================================================
# CUSTOMERS CLEANING
# ============================================================

print("\nCleaning customers...")

# Convert signup date to datetime
customers["signup_date"] = pd.to_datetime(
    customers["signup_date"],
    errors="coerce"
)

# Remove duplicate customer IDs
customers = customers.drop_duplicates(
    subset="customer_id",
    keep="first"
)

# Fill missing age with median age
median_age = customers["age"].median()

customers["age"] = customers["age"].fillna(
    median_age
)

# Convert age to integer
customers["age"] = customers["age"].round().astype(int)


# ============================================================
# PRODUCTS CLEANING
# ============================================================

print("Cleaning products...")

# ------------------------------------------------------------
# Standardize text fields
# ------------------------------------------------------------

products["category"] = (
    products["category"]
    .astype(str)
    .str.strip()
    .str.title()
)

products["subcategory"] = (
    products["subcategory"]
    .astype(str)
    .str.strip()
    .str.title()
)

products["product_name"] = (
    products["product_name"]
    .astype(str)
    .str.strip()
)


# ------------------------------------------------------------
# Correct category mappings using product names
# ------------------------------------------------------------

def infer_category(row):

    current_category = row["category"]
    product_name = row["product_name"].lower()

    # ========================================================
    # ELECTRONICS
    # ========================================================

    electronics_keywords = [
        "smartphone",
        "feature phone",
        "gaming laptop",
        "business laptop",
        "headphones",
        "earbuds",
        "bluetooth speaker",
        "keyboard",
        "mouse",
        "power bank"
    ]

    if any(
        keyword in product_name
        for keyword in electronics_keywords
    ):
        return "Electronics"


    # ========================================================
    # HOME & KITCHEN
    # ========================================================

    home_keywords = [
        "mixer grinder",
        "air fryer",
        "electric kettle",
        "office chair",
        "study table",
        "bookshelf",
        "fan",
        "iron",
        "vacuum cleaner"
    ]

    if any(
        keyword in product_name
        for keyword in home_keywords
    ):
        return "Home & Kitchen"


    # ========================================================
    # FASHION
    # ========================================================

    fashion_keywords = [
        "shirt",
        "jeans",
        "t-shirt",
        "jacket",
        "saree",
        "kurti",
        "dress",
        "running shoes",
        "sandals",
        "formal shoes"
    ]

    if any(
        keyword in product_name
        for keyword in fashion_keywords
    ):
        return "Fashion"


    # ========================================================
    # BEAUTY
    # ========================================================

    beauty_keywords = [
        "face wash",
        "moisturizer",
        "sunscreen",
        "shampoo",
        "hair oil",
        "conditioner",
        "lipstick",
        "foundation",
        "mascara"
    ]

    if any(
        keyword in product_name
        for keyword in beauty_keywords
    ):
        return "Beauty"


    # ========================================================
    # SPORTS
    # ========================================================

    sports_keywords = [
        "yoga mat",
        "dumbbells",
        "resistance bands",
        "cricket bat",
        "football",
        "badminton racket",
        "helmet",
        "cycling gloves",
        "water bottle"
    ]

    if any(
        keyword in product_name
        for keyword in sports_keywords
    ):
        return "Sports"


    # --------------------------------------------------------
    # If no rule matches, keep the existing category
    # --------------------------------------------------------

    return current_category


# ------------------------------------------------------------
# Apply category correction
# ------------------------------------------------------------

original_categories = products["category"].copy()

products["category"] = products.apply(
    infer_category,
    axis=1
)

category_corrections = (
    original_categories != products["category"]
).sum()

print(
    f"Corrected category mappings: "
    f"{category_corrections}"
)


# ------------------------------------------------------------
# Round monetary values
# ------------------------------------------------------------

products["selling_price"] = products[
    "selling_price"
].round(2)

products["cost_price"] = products[
    "cost_price"
].round(2)


# ============================================================
# ORDERS CLEANING
# ============================================================

print("Cleaning orders...")

# Convert order date
orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)

# Remove duplicate order IDs
orders = orders.drop_duplicates(
    subset="order_id",
    keep="first"
)

# Remove invalid quantities
orders = orders[
    orders["quantity"] > 0
].copy()

# Fill missing shipping cost with median
median_shipping = orders[
    "shipping_cost"
].median()

orders["shipping_cost"] = orders[
    "shipping_cost"
].fillna(
    median_shipping
)

# Round shipping cost
orders["shipping_cost"] = orders[
    "shipping_cost"
].round(2)

# Ensure discount is numeric
orders["discount"] = pd.to_numeric(
    orders["discount"],
    errors="coerce"
)

# Fill missing discounts with zero
orders["discount"] = orders[
    "discount"
].fillna(0)

# Standardize payment method
orders["payment_method"] = (
    orders["payment_method"]
    .astype(str)
    .str.strip()
    .str.title()
)

# Standardize region
orders["region"] = (
    orders["region"]
    .astype(str)
    .str.strip()
    .str.title()
)

# Standardize order status
orders["order_status"] = (
    orders["order_status"]
    .astype(str)
    .str.strip()
    .str.title()
)


# ============================================================
# SAVE CLEAN DATA
# ============================================================

customers.to_csv(
    os.path.join(
        CLEAN_DIR,
        "customers_clean.csv"
    ),
    index=False
)

products.to_csv(
    os.path.join(
        CLEAN_DIR,
        "products_clean.csv"
    ),
    index=False
)

orders.to_csv(
    os.path.join(
        CLEAN_DIR,
        "orders_clean.csv"
    ),
    index=False
)


# ============================================================
# CLEANING SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("DATA CLEANING COMPLETE")
print("=" * 70)

print(
    f"Clean customers: {len(customers):,}"
)

print(
    f"Clean products:  {len(products):,}"
)

print(
    f"Clean orders:    {len(orders):,}"
)

print(
    f"Category corrections: {category_corrections}"
)

print("\nFiles saved to:")
print(CLEAN_DIR)

print("=" * 70)
