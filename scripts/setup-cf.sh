#!/usr/bin/env bash
# Setup CloudFoundry CLI tool.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

LOG_FILE="${1:-./logs/discovery-cf.log}"
if [ "$LOG_FILE" != "/dev/stdout" -a "$LOG_FILE" != "/dev/stderr" ]
then
  rm -f "$LOG_FILE"
fi

if [ ! -f /tmp/apt-update-complete ]
then
  echo "> Updating OS package repositories" | tee -a "$LOG_FILE"
  apt-get update >>"$LOG_FILE" 2>&1
  touch /tmp/apt-update-complete >>"$LOG_FILE" 2>&1
fi
if ! which curl >/dev/null
then
  echo "> Installing Cloudfoundry CLI setup dependencies" | tee -a "$LOG_FILE"
  apt-get install -y curl >>"$LOG_FILE" 2>&1
fi

#download and install CloudFoundy CLI if it does not exist
if ! which cf >/dev/null
then
  echo "> Installing the CloudFoundry CLI" | tee -a "$LOG_FILE"
  curl -L -o /tmp/cf-cli_amd64.deb 'https://cli.run.pivotal.io/stable?release=debian64&source=github' >>"$LOG_FILE" 2>&1
  dpkg -i /tmp/cf-cli_amd64.deb >>"$LOG_FILE" 2>&1
  rm -f /tmp/cf-cli_amd64.deb >>"$LOG_FILE" 2>&1
fi

if [ ! -f /usr/local/bin/cf-autopilot ]
then
  echo "> Installing the CloudFoundry Autopilot plugin" | tee -a "$LOG_FILE"  
  curl -L -o /usr/local/bin/cf-autopilot 'https://github.com/contraband/autopilot/releases/download/0.0.4/autopilot-linux' >>"$LOG_FILE" 2>&1
  chmod 755 /usr/local/bin/cf-autopilot >>"$LOG_FILE" 2>&1
  cf install-plugin -f /usr/local/bin/cf-autopilot >>"$LOG_FILE" 2>&1
fi

if [ ! -f /usr/local/bin/cf-antifreeze ]
then
  echo "> Installing the CloudFoundry Antifreeze plugin" | tee -a "$LOG_FILE"  
  curl -L -o /usr/local/bin/cf-antifreeze 'https://github.com/odlp/antifreeze/releases/download/v0.3.0/antifreeze-linux' >>"$LOG_FILE" 2>&1
  chmod 755 /usr/local/bin/cf-antifreeze >>"$LOG_FILE" 2>&1
  cf install-plugin -f /usr/local/bin/cf-antifreeze >>"$LOG_FILE" 2>&1
fi