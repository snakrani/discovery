#!/usr/bin/env bash
# Prepare a python enabled webserver for application hosting.

set -e

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/../app"

LOG_FILE="${1:-$SCRIPT_DIR/../logs/discovery-init.log}"
if [ "$LOG_FILE" != "/dev/stdout" -a "$LOG_FILE" != "/dev/stderr" ]
then
  rm -f "$LOG_FILE"
fi

#activate the virtual python environment
if [ -d /venv ]
then
  alias python="/venv/bin/python"
  source /venv/bin/activate
fi

#run application setup commands

echo "> Collecting Django static files" | tee -a "$LOG_FILE"
python manage.py collectstatic --noinput >>"$LOG_FILE" 2>&1
