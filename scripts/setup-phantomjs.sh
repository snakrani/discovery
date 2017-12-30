#!/usr/bin/env bash
# Setup PhantomJS.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

LOG_FILE="${1:-./logs/discovery-phantomjs.log}"
if [ "$LOG_FILE" != "/dev/stdout" -a "$LOG_FILE" != "/dev/stderr" ]
then
  rm -f "$LOG_FILE"
fi

BIN_DIR="/usr/local/bin"

#download and install PhantomJS if it does not exist
if [ ! -f /usr/local/bin/phantomjs ]
then
  apt-get update >>"$LOG_FILE" 2>&1 

  echo "> Installing PhantomJS dependencies" | tee -a "$LOG_FILE"
  apt-get install -y apt-utils bzip2 wget fontconfig >>"$LOG_FILE" 2>&1
  
  echo "> Downloading and installing PhantomJS" | tee -a "$LOG_FILE"
  wget -O /tmp/phantomjs.tar.bz2 https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 >>"$LOG_FILE" 2>&1
  tar -xjf /tmp/phantomjs.tar.bz2 -C /tmp >>"$LOG_FILE" 2>&1
  mv /tmp/phantomjs-2.1.1-linux-x86_64/bin/phantomjs "$BIN_DIR/phantomjs" >>"$LOG_FILE" 2>&1
  
  apt-get purge -y --auto-remove apt-utils bzip2 wget >>"$LOG_FILE" 2>&1
fi
