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

#set up redis queue
cd /tmp
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
make install

mkdir -p /etc/redis
cp -f redis.conf /etc/redis/6379.conf # binds to 127.0.0.1:6379

sed -i 's/^daemonize\s.*/daemonize yes/' /etc/redis/6379.conf
sed -i 's/^dir\s.*/dir "\/var\/redis\/6379"/' /etc/redis/6379.conf
sed -i 's/^logfile\s.*/logfile "\/var\/log\/redis_6379.log"/' /etc/redis/6379.conf
sed -i 's/^loglevel\s.*/loglevel debug/' /etc/redis/6379.conf

mkdir -p /var/redis/6379

cp -f utils/redis_init_script /etc/init.d/redis # listens at 6379
update-rc.d redis defaults
/etc/init.d/redis start

#set up virtual environment
virtualenv /vagrant/mirage_venv
source /vagrant/mirage_venv/bin/activate
pip install -r /vagrant/requirements.txt

#set up application
source /vagrant/mirage_venv/bin/activate
/vagrant/manage.py syncdb --noinput
/vagrant/manage.py loaddata /vagrant/vendor/fixtures/naics.json
/vagrant/manage.py loaddata /vagrant/vendor/fixtures/setasides.json
/vagrant/manage.py loaddata /vagrant/vendor/fixtures/pools.json
/vagrant/manage.py load_vendors
/vagrant/manage.py runserver 0.0.0.0:8000
