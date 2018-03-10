#!/usr/bin/env bash
# Setup Chrome web driver for Linux.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

LOG_FILE="${1:-./logs/discovery-chrome.log}"
if [ "$LOG_FILE" != "/dev/stdout" -a "$LOG_FILE" != "/dev/stderr" ]
then
  rm -f "$LOG_FILE"
fi

BIN_DIR="/usr/local/bin"
  
apt-get update >>"$LOG_FILE" 2>&1 

echo "> Installing Chrome dependencies" | tee -a "$LOG_FILE"
apt-get install -y wget unzip xvfb libappindicator1 libxss1 libasound2 libx11-xcb1 libminizip1 libwebpmux2 libgtk-3-0 >>"$LOG_FILE" 2>&1

if ! which google-chrome >/dev/null
then
  echo "> Downloading and installing Chrome browser" | tee -a "$LOG_FILE"
  wget -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb >>"$LOG_FILE" 2>&1
  dpkg -i /tmp/chrome.deb >>"$LOG_FILE" 2>&1
  apt --fix-broken install -y
fi

if ! which chromedriver >/dev/null
then
  echo "> Downloading and installing Chrome driver" | tee -a "$LOG_FILE"
  wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/2.36/chromedriver_linux64.zip >>"$LOG_FILE" 2>&1
  unzip /tmp/chromedriver.zip -d "$BIN_DIR" >>"$LOG_FILE" 2>&1
  chmod 755 "$BIN_DIR/chromedriver" >>"$LOG_FILE" 2>&1
fi
