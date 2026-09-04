import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker


# ============================================================
# CONFIGURATION
# ============================================================

random.seed(42)
np.random.seed(42)

fake = Faker("en_IN")
Faker.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

os.makedirs(RAW_DIR, exist_ok=True)

NUM_CUSTOMERS = 5000
NUM_PRODUCTS = 500
NUM_ORDERS = 60000

START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 12, 31)


# ============================================================
# 1. GENERATE CUSTOMERS
# ============================================================

print("Generating customers...")

first_names = [
    "Aarav", "Aditi", "Arjun", "Ananya", "Rahul",
    "Priya", "Rohan", "Sneha", "Vikram", "Neha",
    "Aditya", "Pooja", "Karan", "Kavya", "Amit",
    "Riya", "Nikhil", "Shreya", "Sanjay", "Meera"
]

last_names = [
    "Sharma", "Kumar", "Singh", "Verma", "Gupta",
    "Patel", "Das", "Roy", "Mishra", "Yadav",
    "Jha", "Sinha", "Choudhary", "Shah", "Mehta"
]

indian_cities = {
    "Delhi": "Delhi",
    "Mumbai": "Maharashtra",
    "Bengaluru": "Karnataka",
    "Hyderabad": "Telangana",
    "Chennai": "Tamil Nadu",
    "Kolkata": "West Bengal",
    "Pune": "Maharashtra",
    "Ahmedabad": "Gujarat",
    "Jaipur": "Rajasthan",
    "Lucknow": "Uttar Pradesh",
    "Patna": "Bihar",
    "Bhopal": "Madhya Pradesh",
    "Ranchi": "Jharkhand",
    "Bhubaneswar": "Odisha",
    "Guwahati": "Assam",
    "Chandigarh": "Chandigarh",
    "Indore": "Madhya Pradesh",
    "Nagpur": "Maharashtra",
    "Surat": "Gujarat",
    "Noida": "Uttar Pradesh"
}

customers = []

for i in range(1, NUM_CUSTOMERS + 1):
    city = random.choice(list(indian_cities.keys()))

    signup_days = (END_DATE - START_DATE).days
    signup_date = START_DATE + timedelta(
        days=random.randint(0, signup_days)
    )

    customer = {
        "customer_id": f"CUST{i:05d}",
        "customer_name": (
            f"{random.choice(first_names)} "
            f"{random.choice(last_names)}"
        ),
        "gender": random.choice(["Male", "Female"]),
        "age": random.randint(18, 65),
        "city": city,
        "state": indian_cities[city],
        "signup_date": signup_date.date()
    }

    customers.append(customer)

customers_df = pd.DataFrame(customers)


# ============================================================
# 2. GENERATE PRODUCTS
# ============================================================

print("Generating products...")

product_catalog = {
    "Electronics": {
        "Mobile": ["Smartphone", "Feature Phone"],
        "Laptop": ["Gaming Laptop", "Business Laptop"],
        "Audio": ["Headphones", "Earbuds", "Bluetooth Speaker"],
        "Accessories": ["Keyboard", "Mouse", "Power Bank"]
    },
    "Home & Kitchen": {
        "Kitchen": ["Mixer Grinder", "Air Fryer", "Electric Kettle"],
        "Furniture": ["Office Chair", "Study Table", "Bookshelf"],
        "Appliances": ["Fan", "Iron", "Vacuum Cleaner"]
    },
    "Fashion": {
        "Men": ["Shirt", "Jeans", "T-Shirt", "Jacket"],
        "Women": ["Saree", "Kurti", "Jeans", "Dress"],
        "Footwear": ["Running Shoes", "Sandals", "Formal Shoes"]
    },
    "Beauty": {
        "Skincare": ["Face Wash", "Moisturizer", "Sunscreen"],
        "Haircare": ["Shampoo", "Hair Oil", "Conditioner"],
        "Makeup": ["Lipstick", "Foundation", "Mascara"]
    },
    "Sports": {
        "Fitness": ["Yoga Mat", "Dumbbells", "Resistance Bands"],
        "Outdoor": ["Cricket Bat", "Football", "Badminton Racket"],
        "Cycling": ["Helmet", "Cycling Gloves", "Water Bottle"]
    }
}

products = []

product_id = 1

for category, subcategories in product_catalog.items():

    for subcategory, product_names in subcategories.items():

        for product_name in product_names:

            # Generate multiple variants of each product
            variants = 7

            for variant in range(variants):

                if product_id > NUM_PRODUCTS:
                    break

                base_price = random.randint(300, 80000)

                # Category-specific pricing
                if category == "Fashion":
                    base_price = random.randint(500, 5000)

                elif category == "Beauty":
                    base_price = random.randint(200, 3000)

                elif category == "Sports":
                    base_price = random.randint(300, 10000)

                elif category == "Home & Kitchen":
                    base_price = random.randint(800, 30000)

                cost_price = round(
                    base_price * random.uniform(0.55, 0.85),
                    2
                )

                selling_price = round(
                    base_price * random.uniform(0.95, 1.10),
                    2
                )

                products.append({
                    "product_id": f"PROD{product_id:04d}",
                    "product_name": f"{product_name} {variant + 1}",
                    "category": category,
                    "subcategory": subcategory,
                    "selling_price": selling_price,
                    "cost_price": cost_price
                })

                product_id += 1

            if product_id > NUM_PRODUCTS:
                break

        if product_id > NUM_PRODUCTS:
            break

    if product_id > NUM_PRODUCTS:
        break

products_df = pd.DataFrame(products)


# ============================================================
# 3. GENERATE ORDERS
# ============================================================

print("Generating orders...")

customer_ids = customers_df["customer_id"].tolist()
product_ids = products_df["product_id"].tolist()

regions = {
    "North": ["Delhi", "Jaipur", "Lucknow", "Chandigarh", "Noida"],
    "West": ["Mumbai", "Pune", "Ahmedabad", "Surat", "Indore"],
    "South": ["Bengaluru", "Hyderabad", "Chennai"],
    "East": ["Kolkata", "Patna", "Ranchi", "Bhubaneswar", "Guwahati"]
}

city_to_region = {}

for region, cities in regions.items():
    for city in cities:
        city_to_region[city] = region

product_price_map = products_df.set_index(
    "product_id"
)["selling_price"].to_dict()

orders = []

for i in range(1, NUM_ORDERS + 1):

    customer_id = random.choice(customer_ids)
    product_id = random.choice(product_ids)

    order_days = (END_DATE - START_DATE).days

    order_date = START_DATE + timedelta(
        days=random.randint(0, order_days)
    )

    quantity = random.choices(
        [1, 2, 3, 4, 5],
        weights=[50, 25, 15, 7, 3]
    )[0]

    discount = random.choice([
        0,
        0.05,
        0.10,
        0.15,
        0.20,
        0.25
    ])

    customer_city = customers_df.loc[
        customers_df["customer_id"] == customer_id,
        "city"
    ].iloc[0]

    region = city_to_region.get(
        customer_city,
        random.choice(["North", "South", "East", "West"])
    )

    shipping_cost = round(
        random.uniform(30, 500),
        2
    )

    payment_method = random.choice([
        "UPI",
        "Credit Card",
        "Debit Card",
        "Net Banking",
        "Cash on Delivery",
        "Wallet"
    ])

    order_status = random.choices(
        ["Delivered", "Cancelled", "Returned"],
        weights=[88, 7, 5]
    )[0]

    orders.append({
        "order_id": f"ORD{i:06d}",
        "order_date": order_date.date(),
        "customer_id": customer_id,
        "product_id": product_id,
        "quantity": quantity,
        "discount": discount,
        "shipping_cost": shipping_cost,
        "payment_method": payment_method,
        "region": region,
        "order_status": order_status
    })


orders_df = pd.DataFrame(orders)


# ============================================================
# 4. ADD REAL-WORLD DATA QUALITY ISSUES
# ============================================================

print("Adding realistic data-quality issues...")

# Missing customer ages
missing_age_indices = np.random.choice(
    customers_df.index,
    size=50,
    replace=False
)

customers_df.loc[
    missing_age_indices,
    "age"
] = np.nan


# Duplicate customers
duplicate_customers = customers_df.sample(
    20,
    random_state=42
)

customers_df = pd.concat(
    [customers_df, duplicate_customers],
    ignore_index=True
)


# Invalid quantities
invalid_quantity_indices = np.random.choice(
    orders_df.index,
    size=20,
    replace=False
)

orders_df.loc[
    invalid_quantity_indices,
    "quantity"
] = 0


# Missing shipping costs
missing_shipping_indices = np.random.choice(
    orders_df.index,
    size=100,
    replace=False
)

orders_df.loc[
    missing_shipping_indices,
    "shipping_cost"
] = np.nan


# Duplicate orders
duplicate_orders = orders_df.sample(
    50,
    random_state=42
)

orders_df = pd.concat(
    [orders_df, duplicate_orders],
    ignore_index=True
)


# Inconsistent category spelling
# Intentionally introduce lowercase category values
# while preserving valid category/subcategory relationships.

category_indices = products_df.sample(
    10,
    random_state=42
).index

products_df.loc[
    category_indices,
    "category"
] = products_df.loc[
    category_indices,
    "category"
].str.lower()


# ============================================================
# 5. SAVE DATASETS
# ============================================================

customers_path = os.path.join(
    RAW_DIR,
    "customers.csv"
)

products_path = os.path.join(
    RAW_DIR,
    "products.csv"
)

orders_path = os.path.join(
    RAW_DIR,
    "orders.csv"
)

customers_df.to_csv(
    customers_path,
    index=False
)

products_df.to_csv(
    products_path,
    index=False
)

orders_df.to_csv(
    orders_path,
    index=False
)


# ============================================================
# 6. FINAL SUMMARY
# ============================================================

print()
print("=" * 60)
print("DATA GENERATION COMPLETE")
print("=" * 60)

print(f"Customers: {len(customers_df):,}")
print(f"Products:  {len(products_df):,}")
print(f"Orders:    {len(orders_df):,}")

print()
print("Files created:")

print(customers_path)
print(products_path)
print(orders_path)

print("=" * 60)