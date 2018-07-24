#!/usr/bin/env bash
# Revert the Discovery Dockerized application back to initial empty state
#
# Does not start any application containers, just needed backend services
#
# IMPORTANT: All data will be lost!!!
#

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

# Destroy current environment
"$SCRIPT_DIR/destroy-app.sh"

# Relaunch all the services and initialize the database...
docker-compose up -d data tasks auth
sleep 20
"$SCRIPT_DIR/init-db.sh" /dev/stderr localhost
