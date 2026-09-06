#!/bin/sh

echo "Waiting for PostgreSQL..."

while ! python -c "
import os
import psycopg
psycopg.connect(
    host=os.environ['DB_HOST'],
    port=os.environ['DB_PORT'],
    dbname=os.environ['DB_NAME'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
).close()
" 2>/dev/null
do
    sleep 1
done

echo "PostgreSQL is ready."

python manage.py migrate --noinput

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000