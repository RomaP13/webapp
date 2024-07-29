#!/bin/bash
set -e

# Wait for MySQL to be ready
until mysql -h "db" -u root -p"$MYSQL_ROOT_PASSWORD" -e "SHOW DATABASES;"; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

# Generate init.sql dynamically using environment variables
cat <<EOF > /tmp/init.sql
CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;
CREATE USER IF NOT EXISTS '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';
GRANT ALL PRIVILEGES ON $MYSQL_DATABASE.* TO '$MYSQL_USER'@'%';
FLUSH PRIVILEGES;
EOF

# Run the generated SQL script with root privileges
mysql -h "db" -u root -p"$MYSQL_ROOT_PASSWORD" < /tmp/init.sql

# Run Django migrations
python manage.py makemigrations
python manage.py migrate
