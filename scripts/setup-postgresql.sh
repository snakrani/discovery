#!/usr/bin/env bash
# Setup PhantomJS.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

LOG_FILE="${1:-./logs/discovery-postgresql.log}"
if [ "$LOG_FILE" != "/dev/stdout" -a "$LOG_FILE" != "/dev/stderr" ]
then
  rm -f "$LOG_FILE"
fi

echo "> Installing PostgreSQL package repositories" | tee -a "$LOG_FILE"
echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" > /etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - 2>"$LOG_FILE"
apt-get update >>"$LOG_FILE" 2>&1

#download and install PhantomJS if it does not exist
echo "> Installing PostgreSQL client" | tee -a "$LOG_FILE"
apt-get install -y postgresql-client-9.4 >"$LOG_FILE" 2>&1
