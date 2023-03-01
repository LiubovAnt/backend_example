#!/bin/sh

echo "Waiting for elastic..."
while ! nc -z $ELASTIC_HOST $ELASTIC_PORT; do
  sleep 1
  done
echo "Elastic started"

sleep 10

echo "Waiting for postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
  done
echo "PostgreSQL started"

sleep 10

echo "Start ETL"
python3 main.py

exec "$@"
