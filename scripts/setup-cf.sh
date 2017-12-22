#!/usr/bin/env bash
# Setup CloudFoundry CLI tool.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

#download and install CloudFoundy CLI if it does not exist
if ! which cf > /dev/null
then
  echo "> Installing the CloudFoundry CLI"
  cd /tmp
  curl -s -L -o cf-cli_amd64.deb 'https://cli.run.pivotal.io/stable?release=debian64&source=github'
  sudo dpkg -i cf-cli_amd64.deb > /dev/null
fi

if [ ! -f /usr/local/bin/cf-autopilot ]
then
  echo "> Installing the CloudFoundry Autopilot plugin"  
  sudo curl -s -L -o /usr/local/bin/cf-autopilot 'https://github.com/contraband/autopilot/releases/download/0.0.4/autopilot-linux'
  sudo chmod 755 /usr/local/bin/cf-autopilot
  cf install-plugin -f /usr/local/bin/cf-autopilot > /dev/null
fi

if [ ! -f /usr/local/bin/cf-antifreeze ]
then
  echo "> Installing the CloudFoundry Antifreeze plugin"  
  sudo curl -s -L -o /usr/local/bin/cf-antifreeze 'https://github.com/odlp/antifreeze/releases/download/v0.3.0/antifreeze-linux'
  sudo chmod 755 /usr/local/bin/cf-antifreeze
  cf install-plugin -f /usr/local/bin/cf-antifreeze > /dev/null
fi