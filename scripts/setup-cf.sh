#!/usr/bin/env bash
# Setup CloudFoundry CLI tool.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

LOG_FILE="${1:-./logs/discovery-cf.log}"
if [ "$LOG_FILE" != "/dev/stdout" -a "$LOG_FILE" != "/dev/stderr" ]
then
  rm -f "$LOG_FILE"
fi

PLUGIN_BIN_DIR="/usr/local/bin"

apt-get update >>"$LOG_FILE" 2>&1

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

if [ ! -f "$PLUGIN_BIN_DIR/cf-autopilot" ]
then
  echo "> Installing the CloudFoundry Autopilot plugin" | tee -a "$LOG_FILE"  
  curl -L -o "$PLUGIN_BIN_DIR/cf-autopilot" 'https://github.com/contraband/autopilot/releases/download/0.0.4/autopilot-linux' >>"$LOG_FILE" 2>&1
  chmod 755 "$PLUGIN_BIN_DIR/cf-autopilot" >>"$LOG_FILE" 2>&1
fi

echo "> Adding the CloudFoundry Autopilot plugin for current user" | tee -a "$LOG_FILE"
cf install-plugin -f "$PLUGIN_BIN_DIR/cf-autopilot" >>"$LOG_FILE" 2>&1

if [ ! -f "$PLUGIN_BIN_DIR/cf-service-connect" ]
then
  echo "> Installing the CloudFoundry Service Connect plugin" | tee -a "$LOG_FILE"  
  curl -L -o "$PLUGIN_BIN_DIR/cf-service-connect" 'https://github.com/18F/cf-service-connect/releases/download/1.1.0/cf-service-connect.linux64' >>"$LOG_FILE" 2>&1
  chmod 755 "$PLUGIN_BIN_DIR/cf-service-connect" >>"$LOG_FILE" 2>&1
fi

echo "> Adding the CloudFoundry Service Connect plugin for current user" | tee -a "$LOG_FILE"
cf install-plugin -f "$PLUGIN_BIN_DIR/cf-service-connect" >>"$LOG_FILE" 2>&1
