CREATE DATABASE ecoffee_db;

USE ecoffee_db;

CREATE TABLE product_category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

INSERT INTO product_category (name) VALUES
('Cà phê truyền thống'),
('Cà phê sữa'),
('Trà'),
('Sinh tố'),
('Bánh ngọt');


CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description TEXT,
    image VARCHAR(255),
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES product_category(id)
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('customer', 'staff', 'admin') NOT NULL
);

INSERT INTO users (username, password, role)
VALUES ('admin', '123456','admin'),
       ('customer', '123456','customer');