-- This script creates a table 'users' with attributes id, email, name, and country.
-- The id is an integer, never null, auto increment, and primary key.
-- The email is a string (255 characters), never null, and unique.
-- The name is a string (255 characters).
-- The country is an enumeration of countries: US, CO, and TN, never null with a default value of US.
-- If the table already exists, the script should not fail.

CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);
