#!/usr/bin/env bash
#-------------------------------------------------------------------------------

PROJ_DIR="${1:-/vagrant}"

#-------------------------------------------------------------------------------

#install basic dependencies
if [ ! -f /tmp/apt-update-complete ]
then
  sudo apt-get update
  touch /tmp/apt-update-complete 
fi
sudo apt-get install -y git

#install CloudFoundry CLI
"$PROJ_DIR/scripts/setup-cf.sh"

#set up PostgreSQL database
"$PROJ_DIR/scripts/setup-postgresql.sh"

#set up Redis queue
"$PROJ_DIR/scripts/setup-redis.sh"

#install PhantomJS
"$PROJ_DIR/scripts/setup-phantomjs.sh"

#set up Python
"$PROJ_DIR/scripts/setup-python.sh"
source "$PROJ_DIR/venv/bin/activate"

#set up Django application
"$PROJ_DIR/manage.py" migrate --noinput
"$PROJ_DIR/manage.py" createcachetable
"$PROJ_DIR/manage.py" collectstatic --noinput

#load starter data
"$PROJ_DIR/scripts/load-fixtures.sh"

#create admin user
"$PROJ_DIR/scripts/create-admin.sh" admin admin

#setup background processes
sudo cp -f "$PROJ_DIR/scripts/celery/celery-vars.sh" /etc/default/celery
sudo cp -f "$PROJ_DIR/scripts/celery/celery-init.sh" /etc/init.d/celery
sudo cp -f "$PROJ_DIR/scripts/celery/celerybeat-vars.sh" /etc/default/celerybeat
sudo cp -f "$PROJ_DIR/scripts/celery/celerybeat-init.sh" /etc/init.d/celerybeat

#run applications and services
"$PROJ_DIR/manage.py" runserver "0.0.0.0:8000" &

sudo /etc/init.d/celery restart
sudo /etc/init.d/celerybeat restart
