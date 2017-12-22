#!/usr/bin/env bash
# Deploy the GSA PSHC discovery application development infrastructure.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

set -e # Bomb if anything fails

# Deployment goodness
#
# > CloudFoundry (cloud.gov) with Autopilot and Antifreeze plugins

cf_login() {
  cf login -a "$LOGIN_URL" -u "$DEV_SERVICE_ACCOUNT" -p "$DEV_SERVICE_ACCOUNT_PASSWORD" -o "$DEV_SERVICE_ORG" -s "$DEV_SERVICE_SPACE"  
}

check_app_env() {
  cf check-manifest discovery-dev -f manifest-develop.yml
  cf check-manifest discovery-celerybeat -f manifest-develop.yml
  cf check-manifest discovery-celery -f manifest-develop.yml
}

deploy_app() {
  cf zero-downtime-push discovery-dev -f manifest-develop.yml
  cf push discovery-celerybeat -f manifest-develop.yml
  cf push discovery-celery -f manifest-develop.yml
}

# Check and deploy
cf_login
check_app_env
deploy_app
