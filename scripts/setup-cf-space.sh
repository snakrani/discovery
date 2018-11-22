#!/usr/bin/env bash
# Setup CF services in current space (need Space Developer role)

set -e

SCRIPT_USAGE="
 Usage: <project-dir>/scripts/setup-cf-space.sh [ -h ] [ <cf-org> <cf-space> ] [ <cf-username> ]

  This script will prompt you for the necessary information for getting the 
  Cloud Foundry services setup to run the Discovery application if not provided
  through arguments and options.
  
  If no org, space, and user are given as arguments this script operates in the 
  current org and space without creating a new space.

   -h | --help                |  Display this help message
   -r | --role                |  Update Cloud Foundry space roles only (only run with this flag after initialization) 
   -c | --config              |  Update configurations only (only run with this flag after initialization) 
   -a | --create-account      |  Create a Cloud Foundry space service account and deployment key
  ----|-----------------------|---------------------------------------------------------------------------
   -o | --host=<host[:port]>  |  Discovery application host with port if not 80 (prompt if not specified)
   -k | --key=<API key>       |  Discovery Data.gov API key (prompt if not specified)
   -s | --sam-key=<API key>   |  Discovery Data.gov API key for SAM registration connection (prompt if not specified)
   -n | --hostname=<hostname> |  Discovery application Cloud Foundry hostname (derived from host if not specified)
   -m | --manifest=<branch>   |  Branch name of the Cloud Foundry manifest templates (default: develop)
   -d | --db-plan=<plan>      |  PostgreSQL Cloud Foundry marketplace plan (default: shared-psql) 
   -e | --redis-plan=<plan>   |  Redis queue Cloud Foundry marketplace plan (default: standard)
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

parse_flag '-a|--create-account' CREATE_ACCOUNT || exit 1
parse_flag '-r|--role' ROLE_ONLY || exit 2
parse_flag '-c|--config' CONFIG_ONLY || exit 3

parse_option '-o|--host' DISCOVERY_HOSTNAME validate_string "Discovery host can not be empty if option used" || exit 4
parse_option '-k|--key' API_KEY validate_string "Discovery API key can not be empty if option used" || exit 5
parse_option '-s|--sam-key' SAM_API_KEY validate_string "Discovery SAM API key can not be empty if option used" || exit 6
parse_option '-n|--hostname' WEB_HOSTNAME validate_string "Discovery CF hostname can not be empty if option used" || exit 7
parse_option '-m|--manifest' DEPLOY_MANIFEST validate_string "Discovery CF manifest can not be empty if option used" || exit 8
parse_option '-d|--db-plan' DB_PLAN validate_string "CF PostgreSQL plan can not be empty if option used" || exit 9
parse_option '-e|--redis-plan' REDIS_PLAN validate_string "CF Redis plan can not be empty if option used" || exit 10

ARGS=(`get_args "$PARAMS"`)

DISCOVERY_ORG="${ARGS[0]}"
DISCOVERY_SPACE="${ARGS[1]}"
CF_USER="${ARGS[2]}"

#-------------------------------------------------------------------------------
# Validation

if [ "$DISCOVERY_ORG" ] && [ -z "$DISCOVERY_SPACE" ]
then
  echo "If Discovery organization is given, organization space must also be specified"
  exit 100  
fi

if [ -z "$ROLE_ONLY" ]
then
  if [ -z "$DB_PLAN" ]
  then
    DB_PLAN='shared-psql'
  fi
  if [ -z "$REDIS_PLAN" ]
  then
    REDIS_PLAN='standard'
  fi

  if [ -z "$DEPLOY_MANIFEST" ]
  then
    DEPLOY_MANIFEST='develop'
  fi

  if [ -z "$DISCOVERY_HOSTNAME" ]
  then
    echo "Enter the hostname of the Discovery site (this is a defined Cloud Foundry route)"
    read DISCOVERY_HOSTNAME
    echo ''
  fi
  if ! `echo "$DISCOVERY_HOSTNAME" | grep -q -P '^https?\:\/\/'`
  then
    DISCOVERY_HOSTNAME="https://$DISCOVERY_HOSTNAME"
  fi

  if [ -z "$WEB_HOSTNAME" ]
  then
    WEB_HOSTNAME=`echo "$DISCOVERY_HOSTNAME" | sed -n -r -e 's/^https?\:\/\/([^.]+).*/\1/p'`
  fi

  if [ -z "$API_KEY" ]
  then
    echo "Enter a Data.gov API key for the front end Javascript access to the backend API"
    read API_KEY
    echo ''
  fi

  if [ -z "$SAM_API_KEY" ]
  then
    echo "Enter a Data.gov API key for access to the GSA SAM registration API"
    read SAM_API_KEY
    echo ''
  fi

  if [ -z "$DJANGO_SECRET_KEY" ]
  then
    # Generate a 40 character randomistic string
    DJANGO_SECRET_KEY=`head /dev/urandom | tr -dc A-Za-z0-9 | head -c 40 ; echo ''`
  fi
fi

#-------------------------------------------------------------------------------
# Execution

# Create Discovery development space
if [ "$DISCOVERY_ORG" ]
then
  echo "Creating Cloud Foundry space and role access"
  cf create-space "$DISCOVERY_SPACE" -o "$DISCOVERY_ORG"
  cf target -o "$DISCOVERY_ORG" -s "$DISCOVERY_SPACE"
  
  if [ "$CF_USER" ]
  then
    cf set-space-role "$CF_USER" "$DISCOVERY_ORG" "$DISCOVERY_SPACE" 'SpaceManager'
    cf set-space-role "$CF_USER" "$DISCOVERY_ORG" "$DISCOVERY_SPACE" 'SpaceDeveloper'
  fi
fi

if [ -z "$CONFIG_ONLY" ] && [ -z "$ROLE_ONLY" ]
then
  # Create Discovery service account
  if [ "$CREATE_ACCOUNT" ]
  then
    echo "Creating Cloud.gov service account"
    cf create-service cloud-gov-service-account space-deployer discovery-account
    cf create-service-key discovery-account discovery-key
  fi

  # Create Discovery database
  echo "Creating Discovery database"
  cf create-service aws-rds "$DB_PLAN" discovery-db

  # Create Discovery queues and key stores
  echo "Creating Discovery task queue"
  cf create-service redis32 "$REDIS_PLAN" discovery-tasks
fi

if [ -z "$ROLE_ONLY" ]
then
  # Create Discovery configurations
  app_config="{
  \"API_HOST\": \"$DISCOVERY_HOSTNAME\",
  \"API_KEY\": \"$API_KEY\",
  \"SAM_API_KEY\": \"$SAM_API_KEY\",
  \"SECRET_KEY\": \"$DJANGO_SECRET_KEY\"
}"

  if cf service discovery-config >/dev/null 2>&1
  then
    echo "Updating Discovery configurations"
    cf update-user-provided-service discovery-config -p "$app_config"  
  else
    echo "Creating Discovery configurations"
    cf create-user-provided-service discovery-config -p "$app_config"
  fi

  if [ -z "$CONFIG_ONLY" ]
  then
    echo "Deploying Discovery application"
    source scripts/deploy-base.sh
    deploy_app "$DEPLOY_MANIFEST" "$WEB_HOSTNAME"
  fi
fi
