#!/usr/bin/env bash
# Prepare a Django database for application hosting.

set -e

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

LOG_FILE="${1:-./logs/discovery-init.log}"
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

DB_HOST="${2:-none}"
DB_PORT="${3:-5432}"

if [ "$DB_HOST" != "none" ]
then
  if which git >/dev/null
  then
    git submodule update --init --recursive
  fi
  ./scripts/wait-for-it/wait-for-it.sh --host="$DB_HOST" --port="$DB_PORT"
fi

#run application setup commands

echo "> Migrating Django database structure" | tee -a "$LOG_FILE"
python manage.py migrate --noinput >>"$LOG_FILE" 2>&1

echo "> Ensuring Django cache table" | tee -a "$LOG_FILE"
python manage.py createcachetable >>"$LOG_FILE" 2>&1

echo "> Loading basic category information" | tee -a "$LOG_FILE"
python manage.py load_categories >>"$LOG_FILE" 2>&1

echo "> Clearing outdated locks" | tee -a "$LOG_FILE"
python manage.py clear_locks >>"$LOG_FILE" 2>&1

# Create admin user ONLY IF it doesn't exist yet
./scripts/create-admin.sh admin admin-changeme >>"$LOG_FILE" 2>&1
