#!/usr/bin/env bash

#apt-get update -y
apt-get install -y git
apt-get install -y postgresql-9.3 pgadmin3
apt-get install -y python-pip
apt-get install -y python-virtualenv
apt-get install -y libpq-dev python-dev

#set up database
echo "CREATE USER oasis WITH password 'oasis'; CREATE DATABASE oasis ENCODING 'UTF8' OWNER oasis;" | sudo -u postgres psql
service postgresql restart

#set up virtual environment
virtualenv /vagrant/mirage_venv
source /vagrant/mirage_venv/bin/activate
pip install -r /vagrant/requirements.txt

#set up application
source /vagrant/mirage_venv/bin/activate
/vagrant/manage.py migrate --noinput
/vagrant/manage.py createcachetable
/vagrant/manage.py collectstatic --noinput

/vagrant/manage.py loaddata /vagrant/vendors/fixtures/naics.json
/vagrant/manage.py loaddata /vagrant/vendors/fixtures/setasides.json
/vagrant/manage.py loaddata /vagrant/vendors/fixtures/pools.json
/vagrant/manage.py load_vendors

/vagrant/manage.py runserver 0.0.0.0:8000 &
