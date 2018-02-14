#!/usr/bin/env bash
# Setup Python environment.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

LOG_FILE="${1:-./logs/discovery-python.log}"
if [ "$LOG_FILE" != "/dev/stdout" -a "$LOG_FILE" != "/dev/stderr" ]
then
  rm -f "$LOG_FILE"
fi

VENV_DIR="/venv"

#install Python if it is not installed already
apt-get update >>"$LOG_FILE" 2>&1
  
echo "> Installing Python and CLI utilities" | tee -a "$LOG_FILE"
apt-get install -y make gcc libpq-dev python-dev python-pip git ssh vim >>"$LOG_FILE" 2>&1
rm -rf /var/lib/apt/lists/* >>"$LOG_FILE" 2>&1

#create virtual environment if it does not exist and activate
if [ ! -d "$VENV_DIR" ]
then
  echo "> Creating a Python project virtual environment" | tee -a "$LOG_FILE"
  pip install virtualenv >>"$LOG_FILE" 2>&1
  python -m virtualenv "$VENV_DIR" >>"$LOG_FILE" 2>&1
  
  if [ -f requirements.txt ]
  then
    cp requirements.txt "$VENV_DIR/requirements.txt" >>"$LOG_FILE" 2>&1
  fi
  if [ -f requirements-dev.txt ]
  then
    cp requirements-dev.txt "$VENV_DIR/requirements-dev.txt" >>"$LOG_FILE" 2>&1
  fi
fi
source "$VENV_DIR/bin/activate" >>"$LOG_FILE" 2>&1

#install Python application requirements
echo "> Installing Python project requirements" | tee -a "$LOG_FILE"
pip install -r "$VENV_DIR/requirements.txt" >>"$LOG_FILE" 2>&1
pip install -r "$VENV_DIR/requirements-dev.txt" >>"$LOG_FILE" 2>&1
