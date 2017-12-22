#!/usr/bin/env bash
# Setup local PostgreSQL server.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

#set up database
if [ ! -f /tmp/postgresql ]
then
  if [ ! -f /tmp/apt-update-complete ]
  then
    echo "> Updating OS package repositories"
    sudo apt-get update > /dev/null
    touch /tmp/apt-update-complete 
  fi
  
  echo "> Installing PostgreSQL 9.3 and CLI utilities"
  sudo apt-get install -y postgresql-9.3 pgadmin3 > /dev/null 2>&1
  
  echo "> Modifying PostgreSQL configurations"
  sudo sed -i 's/^#listen_addresses.*/listen_addresses = '"'"'*'"'"'/' /etc/postgresql/9.3/main/postgresql.conf
  grep -q "0.0.0.0/0" /etc/postgresql/9.3/main/pg_hba.conf || echo "host  all  all  0.0.0.0/0  md5" | sudo tee --append /etc/postgresql/9.3/main/pg_hba.conf > /dev/null
  touch /tmp/postgresql
fi

#create oasis user and database and grant ability to create test databases
echo "> Ensuring oasis database and user exist"
echo "CREATE USER oasis WITH password 'oasis'; ALTER USER oasis CREATEDB; CREATE DATABASE oasis ENCODING 'UTF8' OWNER oasis;" | sudo -u postgres psql > /dev/null 2>&1

#start or restart PostgreSQL service
echo "> Starting the PostgreSQL database"
sudo /etc/init.d/postgresql restart > /dev/null