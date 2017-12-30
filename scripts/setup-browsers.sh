#!/usr/bin/env bash
# Setup Browsers.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

LOG_FILE="${1:-./logs/discovery-phantomjs.log}"
if [ "$LOG_FILE" != "/dev/stdout" -a "$LOG_FILE" != "/dev/stderr" ]
then
  rm -f "$LOG_FILE"
fi

BIN_DIR="/usr/local/bin"
  
apt-get update >>"$LOG_FILE" 2>&1 

echo "> Installing web driver dependencies" | tee -a "$LOG_FILE"
apt-get install -y apt-utils wget bzip2 unzip libnss3 libgconf-2-4 libx11-6 libfontconfig1 >>"$LOG_FILE" 2>&1

#download and install PhantomJS if it does not exist
if [ ! -f "$BIN_DIR/phantomjs" ]
then
  echo "> Downloading and installing PhantomJS" | tee -a "$LOG_FILE"
  wget -O /tmp/phantomjs.tar.bz2 https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 >>"$LOG_FILE" 2>&1
  tar -xjf /tmp/phantomjs.tar.bz2 -C /tmp >>"$LOG_FILE" 2>&1
  mv /tmp/phantomjs-2.1.1-linux-x86_64/bin/phantomjs "$BIN_DIR/phantomjs" >>"$LOG_FILE" 2>&1
fi

#download and install Chrome driver if it does not exist
if [ ! -f "$BIN_DIR/chromedriver" ]
then
  echo "> Downloading and installing Chrome web driver" | tee -a "$LOG_FILE"
  wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/2.34/chromedriver_linux64.zip >>"$LOG_FILE" 2>&1
  unzip /tmp/chromedriver.zip -d "$BIN_DIR" >>"$LOG_FILE" 2>&1
fi

#download and install Gecko (Firefox) driver if it does not exist
if [ ! -f "$BIN_DIR/geckodriver" ]
then
  echo "> Downloading and installing Gecko web driver" | tee -a "$LOG_FILE"
  wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz >>"$LOG_FILE" 2>&1
  tar -xzf /tmp/geckodriver.tar.gz -C "$BIN_DIR" >>"$LOG_FILE" 2>&1
fi
