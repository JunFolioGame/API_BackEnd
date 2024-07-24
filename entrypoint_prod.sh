#!/bin/sh


echo "The postgres host  is: $POSTGRES_HOST $POSTGRES_DB_PORT"
# Wait for the DB to be ready
until nc -z -v -w30 $POSTGRES_HOST $(( $POSTGRES_DB_PORT ));
do
 echo 'Waiting for the DB to be ready...'
 sleep 2
done

python manage.py makemigrations
python manage.py migrate
#python manage.py test
python manage.py createsuperuser --no-input
python manage.py initial_data_loading

gunicorn -c gunicorn.py core.wsgi:application
