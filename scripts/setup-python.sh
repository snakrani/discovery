#!/usr/bin/env bash
# Setup Python environment.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

LOG_FILE="${1:-./logs/discovery-python.log}"
if [ "$LOG_FILE" != "/dev/stdout" -a "$LOG_FILE" != "/dev/stderr" ]
then
  rm -f "$LOG_FILE"
fi

#install Python if it is not installed already
if [ ! -f /tmp/apt-update-complete ]
then
  echo "> Updating OS package repositories" | tee -a "$LOG_FILE"
  apt-get update >>"$LOG_FILE" 2>&1
  touch /tmp/apt-update-complete >>"$LOG_FILE" 2>&1 
fi
  
echo "> Installing Python and CLI utilities" | tee -a "$LOG_FILE"
apt-get install -y --no-install-recommends gcc libpq-dev python-dev git >>"$LOG_FILE" 2>&1
rm -rf /var/lib/apt/lists/* >>"$LOG_FILE" 2>&1


#create virtual environment if it does not exist and activate
if [ ! -d /venv ]
then
  echo "> Creating a Python project virtual environment" | tee -a "$LOG_FILE"
  pip install virtualenv >>"$LOG_FILE" 2>&1
  python -m virtualenv /venv >>"$LOG_FILE" 2>&1
  
  if [ -f requirements.txt ]
  then
    cp requirements.txt /venv/requirements.txt >>"$LOG_FILE" 2>&1
  fi
  if [ -f requirements-test.txt ]
  then
    cp requirements-test.txt /venv/requirements-test.txt >>"$LOG_FILE" 2>&1
  fi
fi
source /venv/bin/activate >>"$LOG_FILE" 2>&1

#install Python application requirements
echo "> Installing Python project requirements" | tee -a "$LOG_FILE"
pip install -r /venv/requirements.txt >>"$LOG_FILE" 2>&1
pip install -r /venv/requirements-test.txt >>"$LOG_FILE" 2>&1

#remove all development packages
apt-get purge -y --auto-remove gcc python-dev git >>"$LOG_FILE" 2>&1
