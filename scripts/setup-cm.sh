#!/usr/bin/env bash
# Setup 18F/Open Control Compliance Masonry.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

LOG_FILE="${1:-$SCRIPT_DIR/../logs/discovery-cm.log}"
if [ "$LOG_FILE" != "/dev/stdout" -a "$LOG_FILE" != "/dev/stderr" ]
then
  rm -f "$LOG_FILE"
fi

BIN_DIR="/usr/local/bin"

cd /tmp

echo "> Ensuring Compliance Masonry setup dependencies" | tee -a "$LOG_FILE"
apt-get install -y curl build-essential calibre >>"$LOG_FILE" 2>&1

#download and install Compliance Masonry if it does not exist
if ! which compliance-masonry >/dev/null
then
  echo "> Installing the Compliance Masonry CLI" | tee -a "$LOG_FILE"
  curl -L https://github.com/opencontrol/compliance-masonry/releases/download/v1.1.2/compliance-masonry_1.1.2_linux_amd64.tar.gz -o compliance-masonry.tar.gz >>"$LOG_FILE" 2>&1
  tar -xf compliance-masonry.tar.gz >>"$LOG_FILE" 2>&1
  cp compliance-masonry_1.1.2_linux_amd64/compliance-masonry "$BIN_DIR" >>"$LOG_FILE" 2>&1
fi

#download and install NPM if it does not exist
if ! which npm >/dev/null
then
  echo "> Installing NPM for GitBook support" | tee -a "$LOG_FILE"
  curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash - >>"$LOG_FILE" 2>&1
  apt-get install -y nodejs >>"$LOG_FILE" 2>&1
fi

#download and install Gitbook if it does not exist
if ! which gitbook >/dev/null
then
  echo "> Installing Gitbook CLI" | tee -a "$LOG_FILE"
  npm install -g gitbook-cli >>"$LOG_FILE" 2>&1
fi
