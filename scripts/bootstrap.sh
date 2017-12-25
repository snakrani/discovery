#!/usr/bin/env bash
#-------------------------------------------------------------------------------

PROJ_DIR="${1}" # Required!!
cd "$PROJ_DIR"

#-------------------------------------------------------------------------------

#install basic dependencies
if [ ! -f /tmp/apt-update-complete ]
then
  echo "> Updating OS package repositories"
  sudo apt-get update >/dev/null
  touch /tmp/apt-update-complete 
fi
if ! which git >/dev/null
then
  echo "> Installing Git version control"
  sudo apt-get install -y git >/dev/null 2>&1
fi

#install CloudFoundry CLI
./scripts/setup-cf.sh

#install Docker and Docker Compose
./scripts/setup-docker.sh

#run Docker applications
echo "> Running all Docker services"
docker-compose up -d
