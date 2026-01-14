-- Sample database dump
CREATE TABLE users (id INT, name VARCHAR(50));
INSERT INTO users VALUES (1, 'Alice');
INSERT INTO users VALUES (2, 'Bob');
DELETE FROM users WHERE id = 1;
TRUNCATE TABLE orders;
INSERT INTO orders VALUES (1, 'Order1');
UPDATE users SET name = 'Charlie' WHERE id = 2;
DROP TABLE temp;