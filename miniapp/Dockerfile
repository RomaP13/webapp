FROM python:3.10 as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y default-mysql-client
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv
RUN pipenv install --system --deploy

COPY ngrok.py /app/ngrok.py

# Copy initialization script
COPY init_db.sh /init_db.sh
COPY init.sql /init.sql

RUN chmod +x /init_db.sh

COPY . .
