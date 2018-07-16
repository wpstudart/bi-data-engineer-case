ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';

CREATE DATABASE bi_amaro;

USE bi_amaro;

CREATE TABLE orders (
    id INT NOT NULL,
    user_id INT NOT NULL,
    order_date DATETIME,
    order_subtotal DOUBLE,
    order_discount DOUBLE,
    order_total DOUBLE,
    order_status VARCHAR(20),
    payment_type VARCHAR(20),
    shipping_cost DOUBLE,
    shipping_service VARCHAR(40),
    address_city VARCHAR(40),
    address_state VARCHAR(2),
    utm_source_medium VARCHAR(40),
    device_type VARCHAR(20),
    PRIMARY KEY (id)
);

CREATE TABLE order_items (
    id INT NOT NULL,
    order_id INT NOT NULL,
    sku VARCHAR(100),
    quantity INT,
    code_color VARCHAR(14),
    PRIMARY KEY (id),
    FOREIGN KEY (order_id)
        REFERENCES orders(id)
);


ALTER TABLE orders
	MODIFY order_date varchar(20);
    
DROP TABLE order_items;

DROP TABLE orders;

SELECT * FROM orders LIMIT 15;

SELECT * FROM order_items LIMIT 15;

SELECT orders.id, orders.order_date, orders.order_status, orders.device_type, orders.order_total, order_items.order_id, order_items.code_color
FROM orders LEFT JOIN order_items ON orders.id = order_items.order_id
WHERE orders.order_date = '2016-02-01 00:11:00';

SELECT code_color, COUNT(DISTINCT code_color)
FROM order_items
GROUP BY code_color;

SELECT LEFT(code_color, 8), COUNT(LEFT(code_color, 8))
FROM order_items
GROUP BY code_color;

SELECT code_color, COUNT(code_color)
FROM order_items
GROUP BY code_color;

SELECT order_items.code_color AS code_color, COUNT(order_items.code_color) AS count
FROM orders LEFT JOIN order_items ON orders.id = order_items.order_id
WHERE orders.order_date = '2016-02-01 00:11:00'
GROUP BY order_items.code_color;

SELECT order_items.code_color AS code_color, COUNT(order_items.code_color) AS count
FROM orders LEFT JOIN order_items ON orders.id = order_items.order_id
WHERE orders.order_date = '2016-01-03 13:55:00'
GROUP BY order_items.code_color;

SELECT order_items.code_color AS code_color, COUNT(order_items.code_color) AS count, orders.device_type AS platform
FROM orders LEFT JOIN order_items ON orders.id = order_items.order_id
WHERE orders.order_date = '2016-02-01 00:11:00'
GROUP BY order_items.code_color, orders.device_type;

SELECT order_items.code_color AS code_color, COUNT(order_items.code_color) AS count, orders.device_type AS platform
FROM orders LEFT JOIN order_items ON orders.id = order_items.order_id
WHERE orders.order_date = '2016-02-01 00:11:00' AND orders.device_type='iOS' AND order_items.code_color='20000686_002'
GROUP BY order_items.code_color, orders.device_type;