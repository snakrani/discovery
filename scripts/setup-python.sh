#!/usr/bin/env bash
# Setup Python environment.

set -e

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

LOG_FILE="${1:-./logs/discovery-python.log}"
if [ "$LOG_FILE" != "/dev/stdout" -a "$LOG_FILE" != "/dev/stderr" ]
then
  rm -f "$LOG_FILE"
fi

VENV_DIR="/venv"

if [ ! -f /etc/apt/sources.list.d/testing.list ]
then
  #install Python if it is not installed already
  echo "deb http://ftp.de.debian.org/debian testing main" | tee /etc/apt/sources.list.d/testing.list >>"$LOG_FILE" 2>&1
  echo 'APT::Default-Release "stable";' | tee -a /etc/apt/apt.conf.d/00local >>"$LOG_FILE" 2>&1
fi  

echo "> Installing Python and CLI utilities" | tee -a "$LOG_FILE"
apt-get update >>"$LOG_FILE" 2>&1
apt-get install -y make gcc libdpkg-perl libpq-dev git ssh vim >>"$LOG_FILE" 2>&1
apt-get -t testing -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install python3.6-dev python3.6-venv >>"$LOG_FILE" 2>&1
rm -rf /var/lib/apt/lists/* >>"$LOG_FILE" 2>&1


#create virtual environment if it does not exist and activate
if [ ! -d "$VENV_DIR" ]
then
  echo "> Creating a Python project virtual environment" | tee -a "$LOG_FILE"
  python3 -m venv "$VENV_DIR" >>"$LOG_FILE" 2>&1
fi
  
if [ -f requirements.txt ]
then
  cp requirements.txt "$VENV_DIR/requirements.txt" >>"$LOG_FILE" 2>&1
fi
if [ -f requirements-dev.txt ]
then
  cp requirements-dev.txt "$VENV_DIR/requirements-dev.txt" >>"$LOG_FILE" 2>&1
fi

source "$VENV_DIR/bin/activate" >>"$LOG_FILE" 2>&1

#install Python application requirements
echo "> Installing Python project requirements" | tee -a "$LOG_FILE"
python3 -m pip install -r "$VENV_DIR/requirements.txt" >>"$LOG_FILE" 2>&1
python3 -m pip install -r "$VENV_DIR/requirements-dev.txt" >>"$LOG_FILE" 2>&1
