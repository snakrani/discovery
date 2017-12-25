#!/usr/bin/env bash
# Deploy the GSA PSHC discovery application development infrastructure.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

BIN_DIR="${1:-/usr/local/bin}"


set -e # Bomb if anything fails

source "$SCRIPT_DIR/deploy-base.sh"

# Initialize
#cf_init_plugins "$BIN_DIR"
#cf_login "$DEV_SERVICE_ORG" "$DEV_SERVICE_SPACE" "$DEV_SERVICE_ACCOUNT" "$DEV_SERVICE_ACCOUNT_PASSWORD"

# Deploy
deploy_app develop
