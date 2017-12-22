#!/usr/bin/env bash
# Setup Python environment.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

#install Python if it is not installed already
if ! which python >/dev/null
then
  if [ ! -f /tmp/apt-update-complete ]
  then
    sudo apt-get update
    touch /tmp/apt-update-complete 
  fi
  
  sudo apt-get install -y python-pip
  sudo apt-get install -y python-virtualenv
  sudo apt-get install -y libpq-dev python-dev
fi

#create virtual environment if it does not exist and activate
if [ ! -d venv ]
then
  virtualenv venv
fi
source venv/bin/activate

#install Python application requirements
pip install -r requirements.txt
pip install -r requirements-test.txt