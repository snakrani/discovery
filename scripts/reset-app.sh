#!/usr/bin/env bash
# Revert the Discovery Dockerized application back to initial empty state
#
# IMPORTANT: All data will be lost!!!
#

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

# Destroy current environment
"$SCRIPT_DIR/destroy-app.sh"

# Ensure a fresh Docker environment
docker-compose build

# Relaunch everything...
docker-compose up -d