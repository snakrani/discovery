#!/usr/bin/env bash
# Functions to deploy the GSA PSHC discovery application development infrastructure.

#
# Deployment setup
#
cf_init_plugins() {
  local bin_dir="${1:-/usr/local/bin}"
  
  # In case we are running as a different user as the user who installed CF
  cf install-plugin -f "${bin_dir}/cf-autopilot"
}

cf_login() {
  local org="$1"
  local space="$2"
  local account="$3"
  local password="$4"
  
  cf login -a "$CF_LOGIN_URL" -u "$account" -p "$password" -o "$org" -s "$space"  
}


#
# Deployment execution
#
get_manifest_config() {
  local app="$1"
  local branch="$2"

  echo "cf/manifest-${branch}-${app}.yml"
}

deploy_app() {
  local branch="$1"
  local hostname="$2"
  local fail=0
  
  # Background services
  cf push discovery-scheduler -f "`get_manifest_config scheduler ${branch}`" &
  cf push discovery-worker -f "`get_manifest_config worker ${branch}`" &
  
  # User focused display
  if [ "$hostname" ]
  then
    cf push -n "$hostname" discovery-web -f "`get_manifest_config web ${branch}`" &
  else
    cf zero-downtime-push discovery-web -f "`get_manifest_config web ${branch}`" &
  fi
  
  # Wait on everything to complete
  for job in `jobs -p`
  do
    wait $job || let "fail+=1"
  done
  exit "$fail"
}
