#!/usr/bin/env bash
# Destroy Dockerized application (including stored volume data!!!)
#
# IMPORTANT: All data will be lost!!!
#

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

# Destroy current environment
docker-compose rm --stop --force web scheduler worker
docker-compose down --volumes
