-- script to manage TaskHub Database

CREATE DATABASE IF NOT EXISTS taskhub_dev_db;
CREATE DATABASE IF NOT EXISTS taskhub_test_db;
CREATE USER IF NOT EXISTS 'taskhub_dev'@'localhost' IDENTIFIED BY 'taskhub_dev_pwd';
GRANT ALL ON taskhub_dev_db.* TO 'taskhub_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'taskhub_dev'@'localhost';
CREATE USER IF NOT EXISTS 'taskhub_test'@'localhost' IDENTIFIED BY 'taskhub_test_pwd';
GRANT ALL ON taskhub_test_db.* TO 'taskhub_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'taskhub_test'@'localhost';