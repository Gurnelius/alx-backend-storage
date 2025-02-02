-- Task 4: Create Trigger to Decrease Item Quantity
-- This script creates a trigger that decreases the quantity of an item after adding a new order.
-- The quantity in the table 'items' can be negative.

-- Create the initial tables
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS orders;

CREATE TABLE IF NOT EXISTS items (
    name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL DEFAULT 10
);

CREATE TABLE IF NOT EXISTS orders (
    item_name VARCHAR(255) NOT NULL,
    number INT NOT NULL
);

-- Insert initial data
INSERT INTO items (name) VALUES ('apple'), ('pineapple'), ('pear');

-- Create the trigger
DELIMITER //

CREATE TRIGGER decrease_quantity AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items SET quantity = quantity - NEW.number WHERE name = NEW.item_name;
END//

DELIMITER ;
