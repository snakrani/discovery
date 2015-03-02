#!/bin/bash
echo "------ Create database tables ------"
python manage.py migrate --noinput
wget https://s3.amazonaws.com/mirage-gsa-gov/discovery.sql.gz
gunzip discovery.sql.gz
psql discovery < discovery.sql

waitress-serve --port=$VCAP_APP_PORT discovery.wsgi:application
