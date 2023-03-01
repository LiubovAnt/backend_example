#!/bin/sh

echo "Waiting for elastic..."

while ! nc -z $ELASTIC_HOST $ELASTIC_PORT; do
  sleep 0.1
done
echo "Elastic started"

echo "Start ETL"

echo "Waiting for redis..."

while ! nc -z $REDIS_HOST $REDIS_PORT; do
  sleep 0.1
done
echo "Redis started"

echo "Start API"

exec "$@"
