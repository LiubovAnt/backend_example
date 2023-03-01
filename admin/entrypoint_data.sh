#!/bin/sh

echo "Waiting for DB..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "DB started"

sleep 10

echo "Load data"
python /data/loader/main.py

echo "Test data"
pytest 

exec "$@"