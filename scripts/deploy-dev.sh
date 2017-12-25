#!/usr/bin/env bash
# Deploy the GSA PSHC discovery application development infrastructure.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

set -e # Bomb if anything fails

# Deployment goodness
#
# > CloudFoundry (cloud.gov) with Autopilot and Antifreeze plugins

cf_init_plugins() {
  # In case we are running as a different user as the user who installed CF
  cf install-plugin -f /usr/local/bin/cf-autopilot
  cf install-plugin -f /usr/local/bin/cf-antifreeze
}

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

# Initialize
cf_init_plugins
cf_login

# Check and deploy
check_app_env
deploy_app
