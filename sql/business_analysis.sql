-- ============================================
-- E-Commerce Business Analytics
-- SQL Analysis
-- ============================================

-- 1. Total Orders
SELECT COUNT(*) AS total_orders
FROM orders;


-- 2. Total Customers
SELECT COUNT(*) AS total_customers
FROM customers;


-- 3. Total Products
SELECT COUNT(*) AS total_products
FROM products;


-- 4. Orders by Status
SELECT
    order_status,
    COUNT(*) AS order_count
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;


-- 5. Sales by Payment Method
SELECT
    payment_method,
    COUNT(*) AS orders,
    ROUND(
        SUM(quantity * (SELECT selling_price
                        FROM products
                        WHERE products.product_id = orders.product_id)
            * (1 - discount / 100)),
        2
    ) AS net_sales
FROM orders
GROUP BY payment_method
ORDER BY net_sales DESC;


-- 6. Orders by Region
SELECT
    region,
    COUNT(*) AS orders
FROM orders
GROUP BY region
ORDER BY orders DESC;


-- 7. Sales by Region
SELECT
    o.region,
    ROUND(
        SUM(
            o.quantity * p.selling_price * (1 - o.discount / 100)
        ),
        2
    ) AS net_sales
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY o.region
ORDER BY net_sales DESC;


-- 8. Orders by Year
SELECT
    strftime('%Y', order_date) AS year,
    COUNT(*) AS orders
FROM orders
GROUP BY year
ORDER BY year;


-- 9. Sales by Year
SELECT
    strftime('%Y', o.order_date) AS year,
    ROUND(
        SUM(
            o.quantity * p.selling_price * (1 - o.discount / 100)
        ),
        2
    ) AS net_sales
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY year
ORDER BY year;


-- 10. Top 10 Products by Sales
SELECT
    o.product_id,
    p.product_name,
    p.category,
    p.subcategory,
    ROUND(
        SUM(
            o.quantity * p.selling_price * (1 - o.discount / 100)
        ),
        2
    ) AS net_sales
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY
    o.product_id,
    p.product_name,
    p.category,
    p.subcategory
ORDER BY net_sales DESC
LIMIT 10;


-- 11. Sales by Category
SELECT
    p.category,
    ROUND(
        SUM(
            o.quantity * p.selling_price * (1 - o.discount / 100)
        ),
        2
    ) AS net_sales,
    SUM(o.quantity) AS quantity_sold
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY net_sales DESC;


-- 12. Sales by Category and Year
SELECT
    strftime('%Y', o.order_date) AS year,
    p.category,
    ROUND(
        SUM(
            o.quantity * p.selling_price * (1 - o.discount / 100)
        ),
        2
    ) AS net_sales
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY year, p.category
ORDER BY year, net_sales DESC;


-- 13. Top 10 Customers by Sales
SELECT
    o.customer_id,
    COUNT(*) AS orders,
    ROUND(
        SUM(
            o.quantity * p.selling_price * (1 - o.discount / 100)
        ),
        2
    ) AS net_sales
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY o.customer_id
ORDER BY net_sales DESC
LIMIT 10;


-- 14. Average Order Value
SELECT
    ROUND(
        SUM(
            o.quantity * p.selling_price * (1 - o.discount / 100)
        )
        / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM orders o
JOIN products p
    ON o.product_id = p.product_id;


-- 15. Average Order Quantity
SELECT
    ROUND(AVG(quantity), 2) AS average_quantity_per_order
FROM orders;


-- 16. Monthly Sales Trend
SELECT
    strftime('%Y-%m', o.order_date) AS month,
    ROUND(
        SUM(
            o.quantity * p.selling_price * (1 - o.discount / 100)
        ),
        2
    ) AS net_sales
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY month
ORDER BY month;


-- 17. Customer Order Frequency
SELECT
    customer_id,
    COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
ORDER BY order_count DESC;


-- 18. Product Performance
SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(o.quantity) AS units_sold,
    ROUND(
        SUM(
            o.quantity * p.selling_price * (1 - o.discount / 100)
        ),
        2
    ) AS net_sales
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY net_sales DESC
LIMIT 20;