"""
SQL Queries Practice Solution

Common SQL queries for backend interview preparation covering:
- Basic SELECT statements
- JOINs (INNER, LEFT, RIGHT, FULL)
- Aggregations (COUNT, SUM, AVG, GROUP BY)
- Subqueries and CTEs
- Window functions
- Data modification (INSERT, UPDATE, DELETE)

Note: This file contains SQL query examples as strings for reference.
In practice, you would execute these against a database.
"""

# Sample database schema for reference:
"""
Users table:
- id (INTEGER PRIMARY KEY)
- name (VARCHAR)
- email (VARCHAR)
- created_at (TIMESTAMP)

Orders table:
- id (INTEGER PRIMARY KEY)
- user_id (INTEGER FOREIGN KEY REFERENCES Users(id))
- product_name (VARCHAR)
- amount (DECIMAL)
- order_date (TIMESTAMP)

Products table:
- id (INTEGER PRIMARY KEY)
- name (VARCHAR)
- price (DECIMAL)
- category (VARCHAR)
"""

# 1. Basic SELECT queries
BASIC_SELECT = """
-- Get all users
SELECT * FROM Users;

-- Get specific columns
SELECT id, name, email FROM Users;

-- Get users created in last 30 days
SELECT * FROM Users 
WHERE created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY);

-- Get users with specific email domain
SELECT * FROM Users 
WHERE email LIKE '%@gmail.com';
"""

# 2. JOIN queries
JOIN_QUERIES = """
-- INNER JOIN: Users with their orders
SELECT u.name, o.product_name, o.amount, o.order_date
FROM Users u
INNER JOIN Orders o ON u.id = o.user_id
ORDER BY o.order_date DESC;

-- LEFT JOIN: All users and their orders (including users without orders)
SELECT u.name, o.product_name, o.amount
FROM Users u
LEFT JOIN Orders o ON u.id = o.user_id
WHERE o.id IS NOT NULL;  -- Only users with orders

-- LEFT JOIN including users without orders
SELECT u.name, o.product_name, o.amount
FROM Users u
LEFT JOIN Orders o ON u.id = o.user_id;

-- Multiple JOINs: Users, Orders, and Products
SELECT u.name, o.amount, p.name as product_name, p.category
FROM Users u
INNER JOIN Orders o ON u.id = o.user_id
INNER JOIN Products p ON o.product_name = p.name;
"""

# 3. Aggregation queries
AGGREGATION_QUERIES = """
-- Count total users
SELECT COUNT(*) as total_users FROM Users;

-- Count orders per user
SELECT u.name, COUNT(o.id) as order_count
FROM Users u
LEFT JOIN Orders o ON u.id = o.user_id
GROUP BY u.id, u.name
ORDER BY order_count DESC;

-- Average order amount per user
SELECT u.name, AVG(o.amount) as avg_order_amount
FROM Users u
INNER JOIN Orders o ON u.id = o.user_id
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 0;

-- Total revenue by month
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') as month,
    SUM(amount) as monthly_revenue
FROM Orders
GROUP BY month
ORDER BY month;

-- Users with more than 5 orders
SELECT u.name, COUNT(o.id) as order_count
FROM Users u
INNER JOIN Orders o ON u.id = o.user_id
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 5;
"""

# 4. Subqueries and CTEs
SUBQUERY_CTE_QUERIES = """
-- Subquery: Users who placed orders in the last month
SELECT * FROM Users
WHERE id IN (
    SELECT user_id FROM Orders 
    WHERE order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)
);

-- CTE: Monthly user activity
WITH MonthlyActivity AS (
    SELECT 
        user_id,
        DATE_FORMAT(order_date, '%Y-%m') as month,
        COUNT(*) as order_count,
        SUM(amount) as total_spent
    FROM Orders
    GROUP BY user_id, month
)
SELECT 
    u.name,
    ma.month,
    ma.order_count,
    ma.total_spent
FROM Users u
JOIN MonthlyActivity ma ON u.id = ma.user_id
ORDER BY ma.month DESC, ma.total_spent DESC;

-- Subquery with aggregation: Users spending above average
SELECT u.name, u.email
FROM Users u
WHERE u.id IN (
    SELECT o.user_id
    FROM Orders o
    GROUP BY o.user_id
    HAVING SUM(o.amount) > (
        SELECT AVG(total_spent) FROM (
            SELECT SUM(amount) as total_spent
            FROM Orders
            GROUP BY user_id
        ) as user_totals
    )
);
"""

# 5. Window functions
WINDOW_FUNCTION_QUERIES = """
-- Running total of orders per user
SELECT 
    u.name,
    o.order_date,
    o.amount,
    SUM(o.amount) OVER (PARTITION BY u.id ORDER BY o.order_date) as running_total
FROM Users u
INNER JOIN Orders o ON u.id = o.user_id
ORDER BY u.name, o.order_date;

-- Rank users by total spending
SELECT 
    u.name,
    SUM(o.amount) as total_spent,
    RANK() OVER (ORDER BY SUM(o.amount) DESC) as spending_rank
FROM Users u
INNER JOIN Orders o ON u.id = o.user_id
GROUP BY u.id, u.name
ORDER BY spending_rank;

-- Previous order amount for each user (LAG)
SELECT 
    u.name,
    o.order_date,
    o.amount,
    LAG(o.amount) OVER (PARTITION BY u.id ORDER BY o.order_date) as prev_order_amount
FROM Users u
INNER JOIN Orders o ON u.id = o.user_id
ORDER BY u.name, o.order_date;
"""

# 6. Data modification queries
DATA_MODIFICATION_QUERIES = """
-- Insert new user
INSERT INTO Users (name, email, created_at)
VALUES ('John Doe', 'john@example.com', NOW());

-- Update user email
UPDATE Users 
SET email = 'newemail@example.com'
WHERE id = 1;

-- Delete inactive users (no orders in last year)
DELETE FROM Users
WHERE id NOT IN (
    SELECT DISTINCT user_id 
    FROM Orders 
    WHERE order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR)
);

-- Update order status (assuming status column exists)
UPDATE Orders
SET status = 'completed'
WHERE order_date < DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
  AND status = 'pending';
"""

def print_sql_examples():
    """Print all SQL query examples for reference."""
    print("=== BASIC SELECT QUERIES ===")
    print(BASIC_SELECT.strip())
    print("\n=== JOIN QUERIES ===")
    print(JOIN_QUERIES.strip())
    print("\n=== AGGREGATION QUERIES ===")
    print(AGGREGATION_QUERIES.strip())
    print("\n=== SUBQUERY AND CTE QUERIES ===")
    print(SUBQUERY_CTE_QUERIES.strip())
    print("\n=== WINDOW FUNCTION QUERIES ===")
    print(WINDOW_FUNCTION_QUERIES.strip())
    print("\n=== DATA MODIFICATION QUERIES ===")
    print(DATA_MODIFICATION_QUERIES.strip())

if __name__ == "__main__":
    print_sql_examples()
    
    # Study tips for SQL interviews
    print("\n" + "="*50)
    print("SQL INTERVIEW TIPS:")
    print("="*50)
    print("1. Always consider NULL values in JOIN conditions")
    print("2. Use LEFT JOIN when you want to keep all records from left table")
    print("3. Remember the order: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY")
    print("4. Use EXISTS instead of IN for better performance with subqueries")
    print("5. Index columns used in JOIN, WHERE, and ORDER BY clauses")
    print("6. Practice explaining your query logic step by step")
    print("7. Know the difference between INNER and OUTER joins")
    print("8. Understand when to use GROUP BY vs DISTINCT")