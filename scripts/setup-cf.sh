#!/usr/bin/env bash
# Setup CloudFoundry CLI tool.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

#download and install CloudFoundy CLI if it does not exist
if ! which cf > /dev/null
then
  cd /tmp
  curl -v -L -o cf-cli_amd64.deb 'https://cli.run.pivotal.io/stable?release=debian64&source=github'
  sudo dpkg -i cf-cli_amd64.deb
fi