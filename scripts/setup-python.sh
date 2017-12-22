#!/usr/bin/env bash
# Setup Python environment.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

#install Python if it is not installed already
if ! which python >/dev/null
then
  if [ ! -f /tmp/apt-update-complete ]
  then
    echo "> Updating OS package repositories"
    sudo apt-get update > /dev/null
    touch /tmp/apt-update-complete 
  fi
  
  echo "> Installing Python and CLI utilities"
  sudo apt-get install -y python-pip > /dev/null
  sudo apt-get install -y python-virtualenv > /dev/null
  sudo apt-get install -y libpq-dev python-dev > /dev/null
fi

#create virtual environment if it does not exist and activate
if [ ! -d venv ]
then
  echo "> Creating a Python project virtual environment"
  virtualenv venv > /dev/null
fi
source venv/bin/activate

#install Python application requirements
echo "> Installing Python project requirements"
pip install -r requirements.txt > /dev/null
pip install -r requirements-test.txt > /dev/null