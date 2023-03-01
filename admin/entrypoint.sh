#!/bin/sh

echo "Waiting for DB..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "DB started"

python manage.py migrate --fake movies 0001
python manage.py migrate movies 0002
python manage.py migrate --fake movies 0002
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input --clear
python manage.py createsuperuser --noinput

exec "$@"