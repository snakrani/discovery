#!/usr/bin/env bash
# Deploy the GSA PSHC discovery application production infrastructure.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

BIN_DIR="${1:-/usr/local/bin}"


set -e # Bomb if anything fails

source "$SCRIPT_DIR/deploy-base.sh"

# Initialize
cf_init_plugins "$BIN_DIR"
cf_login "$PROD_SERVICE_ORG" "$PROD_SERVICE_SPACE" "$PROD_SERVICE_ACCOUNT" "$PROD_SERVICE_ACCOUNT_PASSWORD" 

# Deploy
deploy_app master
