#!/usr/bin/env bash
# Clear and destroy a Cloud Foundry space

set -e

SCRIPT_USAGE="
 Usage: <project-dir>/scripts/delete-cf-space.sh [ -h ] <cf-org> <cf-space>

  This script will remove all Discovery related applications, services, and 
routes before deleting the Cloud Foundry space specified.

   -h | --help  |  Display this help message
"

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

source "$SCRIPT_DIR/bash-opts.sh"
source "$SCRIPT_DIR/bash-validators.sh"

#-------------------------------------------------------------------------------
# Argument / Options

PARAMS=`normalize_params "$@"`

parse_flag '-h|--help' HELP_WANTED

if [ "$HELP_WANTED" ]
then
  echo "$SCRIPT_USAGE"
  exit 0
fi

ARGS=(`get_args "$PARAMS"`)

DISCOVERY_ORG="${ARGS[0]}"
DISCOVERY_SPACE="${ARGS[1]}"

#-------------------------------------------------------------------------------
# Validation

if [ -z "$DISCOVERY_ORG" -o -z "$DISCOVERY_SPACE" ]
then
  echo "Discovery organization and space must be specified"
  exit 100  
fi 

#-------------------------------------------------------------------------------
# Execution

# Target the correct space
cf target -o "$DISCOVERY_ORG" -s "$DISCOVERY_SPACE"

# Delete applications
echo "Deleting Discovery applications"
cf delete -f discovery-scheduler
cf delete -f discovery-worker
cf delete -f discovery-web

# Delete related services
echo "Deleting Discovery services"
cf delete-service -f discovery-config
cf delete-service -f discovery-tasks
cf delete-service -f discovery-db

# Delete service account and service key
echo "Deleting service account and key"
cf delete-service-key -f discovery-account discovery-key
cf delete-service -f discovery-account

# Delete orphaned routes
echo "Deleting Discovery routes"
cf delete-orphaned-routes -f

# Delete organization space
echo "Deleting Cloud Foundry space"
cf delete-space "$DISCOVERY_SPACE" -o "$DISCOVERY_ORG" -f
