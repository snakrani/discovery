#!/usr/bin/env bash
#-------------------------------------------------------------------------------

PROJ_DIR="${1}" # Required!!
ADMIN_USER="${2:-admin}"
ADMIN_PASSWORD="${3:-admin}"
ADMIN_EMAIL="${4:-admin@example.com}"

#-------------------------------------------------------------------------------

#install basic dependencies
if [ ! -f /tmp/apt-update-complete ]
then
  echo "> Updating OS package repositories"
  sudo apt-get update > /dev/null
  touch /tmp/apt-update-complete 
fi
if ! which git > /dev/null
then
  echo "> Installing Git version control"
  sudo apt-get install -y git > /dev/null 2>&1
fi

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

#set up Django application
"$PROJ_DIR/scripts/init-server.sh"

#create admin user
"$PROJ_DIR/scripts/create-admin.sh" "$ADMIN_USER" "$ADMIN_PASSWORD" "$ADMIN_EMAIL"

#setup background processes
echo "> Copying Celery service configurations and scripts"
sudo cp -f "$PROJ_DIR/scripts/celery/celery-vars.sh" /etc/default/celery
sudo cp -f "$PROJ_DIR/scripts/celery/celery-init.sh" /etc/init.d/celery
sudo cp -f "$PROJ_DIR/scripts/celery/celerybeat-vars.sh" /etc/default/celerybeat
sudo cp -f "$PROJ_DIR/scripts/celery/celerybeat-init.sh" /etc/init.d/celerybeat

#run applications and services
echo "> Starting the Django web application"
source "$PROJ_DIR/venv/bin/activate"
"$PROJ_DIR/manage.py" runserver "0.0.0.0:8000" &

echo "> Starting the Celery worker"
sudo /etc/init.d/celery restart > /dev/null
  
echo "> Starting the Celery scheduler"
sudo /etc/init.d/celerybeat restart > /dev/null
