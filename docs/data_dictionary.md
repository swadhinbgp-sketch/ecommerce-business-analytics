# Data Dictionary

## Customers Table

| Column | Data Type | Description |
|---|---|---|
| customer_id | String | Unique customer identifier |
| customer_name | String | Customer name |
| gender | String | Customer gender |
| age | Integer | Customer age |
| city | String | Customer city |
| state | String | Customer state |
| signup_date | Date | Customer registration date |

## Products Table

| Column | Data Type | Description |
|---|---|---|
| product_id | String | Unique product identifier |
| product_name | String | Product name |
| category | String | Main product category |
| subcategory | String | Product subcategory |
| selling_price | Decimal | Product selling price |
| cost_price | Decimal | Product cost price |

## Orders Table

| Column | Data Type | Description |
|---|---|---|
| order_id | String | Unique order identifier |
| order_date | Date | Date of purchase |
| customer_id | String | Customer identifier |
| product_id | String | Product identifier |
| quantity | Integer | Number of units purchased |
| discount | Decimal | Discount applied |
| shipping_cost | Decimal | Shipping cost |
| payment_method | String | Payment method |
| region | String | Sales region |
| order_status | String | Order status |