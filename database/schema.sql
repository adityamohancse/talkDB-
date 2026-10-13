-- database/schema.sql

-- Products table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    sku VARCHAR(50) UNIQUE NOT NULL,
    cost_price DECIMAL(10,2) NOT NULL,
    selling_price DECIMAL(10,2) NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    reorder_level INTEGER NOT NULL DEFAULT 10,
    supplier VARCHAR(200)
);

-- Sales table
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(product_id),
    quantity_sold INTEGER NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    sale_date DATE NOT NULL,
    store_location VARCHAR(100) NOT NULL,
    payment_method VARCHAR(50) NOT NULL
);

-- Inventory movements
CREATE TABLE inventory_log (
    log_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(product_id),
    movement_type VARCHAR(20) NOT NULL,
    quantity INTEGER NOT NULL,
    reason VARCHAR(100) NOT NULL,
    log_date DATE NOT NULL
);

-- Customers table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    phone VARCHAR(20),
    total_purchases DECIMAL(10,2) DEFAULT 0,
    visit_count INTEGER DEFAULT 0,
    last_visit DATE
);