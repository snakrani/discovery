#!/usr/bin/env bash
#-------------------------------------------------------------------------------

PROJ_DIR="${1:-/vagrant}"

#-------------------------------------------------------------------------------

function keep_alive() {
  PID_FILE="/tmp/$1.pid"
  
  if [ -f "$PID_FILE" ]
  then
      PID=`cat "$PID_FILE"`
      
      if ! kill -0 $PID 2>/dev/null
      then
        echo "Restarting: $1"
        "${@:2}" &
        echo "$!" > "$PID_FILE"        
      fi
  else
    echo "Creating: $1"
    "${@:2}" &
    echo "$!" > "$PID_FILE"    
  fi
}

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
service postgresql restart

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
/etc/init.d/redis restart

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

"$PROJ_DIR/scripts/load-fixtures.sh"

#run application
keep_alive site "$PROJ_DIR/manage.py" runserver 0.0.0.0:8000
keep_alive processor celery -A discovery worker --loglevel=info --concurrency=1
keep_alive scheduler celery -A discovery beat --loglevel=info
