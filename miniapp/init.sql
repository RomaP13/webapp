CREATE DATABASE IF NOT EXISTS trading_app;
CREATE USER IF NOT EXISTS 'mysql_user'@'%' IDENTIFIED BY 'mysql_user_password123';
GRANT ALL PRIVILEGES ON trading_app.* TO 'mysql_user'@'%';
FLUSH PRIVILEGES;
