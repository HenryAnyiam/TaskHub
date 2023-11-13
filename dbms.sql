-- script to manage TaskHub Database

CREATE DATABASE IF NOT EXISTS taskhub_dev_db;
CREATE DATABASE IF NOT EXISTS taskhub_test_db;
CREATE USER IF NOT EXISTS 'taskhub_dev'@'localhost' IDENTIFIED BY 'taskhub_dev_pwd';
CREATE USER IF NOT EXISTS 'taskhub_test'@'localhost' IDENTIFIED BY 'taskhub_test_pwd';