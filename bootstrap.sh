#!/usr/bin/env bash

#apt-get update -y
apt-get install -y git
apt-get install -y postgresql-9.3 pgadmin3
apt-get install -y python-pip
apt-get install -y python-virtualenv
apt-get install -y libpq-dev python-dev

#set up database
echo "CREATE ROLE oasis LOGIN password 'secret'; CREATE DATABASE oasis ENCODING 'UTF8' OWNER oasis;" | sudo -u postgres psql
/etc/init.d/postgresql restart

#set up application
virtualenv /vagrant/mirage_venv
source /vagrant/mirage_venv/bin/activate
pip install -r /vagrant/requirements.txt
