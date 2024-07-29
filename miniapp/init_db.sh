#!/bin/bash
set -e

# Wait for MySQL to be ready
until mysql -h "db" -u root -e "SHOW DATABASES;"; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

# Run initial SQL script with root privileges
mysql -h "db" -u root < init.sql

# Run Django migrations
python manage.py makemigrations
python manage.py migrate
