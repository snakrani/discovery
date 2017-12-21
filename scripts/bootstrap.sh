#!/usr/bin/env bash
#-------------------------------------------------------------------------------

PROJ_DIR="${1:-/vagrant}"

#-------------------------------------------------------------------------------

#install dependencies
apt-get update
apt-get install -y git
apt-get install -y postgresql-9.3 pgadmin3
apt-get install -y python-pip
apt-get install -y python-virtualenv
apt-get install -y libpq-dev python-dev
apt-get install -y fontconfig wget

#set up database
if [ ! -f /tmp/postgresql ]
then
  sed -i 's/^#listen_addresses.*/listen_addresses = '"'"'*'"'"'/' /etc/postgresql/9.3/main/postgresql.conf
  grep -q "0.0.0.0/0" /etc/postgresql/9.3/main/pg_hba.conf || echo "host  all  all  0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf
  touch /tmp/postgresql
fi
echo "CREATE USER oasis WITH password 'oasis'; ALTER USER oasis CREATEDB; CREATE DATABASE oasis ENCODING 'UTF8' OWNER oasis;" | sudo -u postgres psql

#set up redis queue
if [ ! -f /etc/init.d/redis ]
then
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
fi

#set up virtual environment
if [ ! -d "$PROJ_DIR/venv" ]
then
  virtualenv "$PROJ_DIR/venv"
fi
source "$PROJ_DIR/venv/bin/activate"
pip install -r "$PROJ_DIR/requirements.txt"
pip install -r "$PROJ_DIR/requirements-test.txt"

#install phantomJS
if [ ! -f "$PROJ_DIR/venv/bin/phantomjs" ]
then
  wget -O /tmp/phantomjs.tar.bz2 https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
  tar -xjf /tmp/phantomjs.tar.bz2 -C /tmp
  mv /tmp/phantomjs-2.1.1-linux-x86_64/bin/phantomjs "$PROJ_DIR/venv/bin/phantomjs"
fi

#set up application
"$PROJ_DIR/manage.py" migrate --noinput
"$PROJ_DIR/manage.py" createcachetable
"$PROJ_DIR/manage.py" collectstatic --noinput

#create admin user
echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | "$PROJ_DIR/manage.py" shell

#load starter data
"$PROJ_DIR/scripts/load-fixtures.sh"

#setup background processes
cp -f "$PROJ_DIR/scripts/bootstrap/celery-vars.sh" /etc/default/celery
cp -f "$PROJ_DIR/scripts/bootstrap/celery-init.sh" /etc/init.d/celery
cp -f "$PROJ_DIR/scripts/bootstrap/celerybeat-vars.sh" /etc/default/celerybeat
cp -f "$PROJ_DIR/scripts/bootstrap/celerybeat-init.sh" /etc/init.d/celerybeat

#run applications and services
/etc/init.d/postgresql restart

/etc/init.d/redis stop
/etc/init.d/redis start

"$PROJ_DIR/manage.py" runserver "0.0.0.0:8000" &
/etc/init.d/celery restart
/etc/init.d/celerybeat restart
