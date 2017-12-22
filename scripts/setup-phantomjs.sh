#!/usr/bin/env bash
# Setup PhantomJS.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

#download and install PhantomJS if it does not exist
if [ ! -f venv/bin/phantomjs ]
then
  if [ ! -f /tmp/apt-update-complete ]
  then
    echo "> Updating OS package repositories"
    sudo apt-get update > /dev/null
    touch /tmp/apt-update-complete 
  fi
  echo "> Installing FontConfig library"
  sudo apt-get install -y fontconfig > /dev/null
  
  echo "> Downloading and installing PhantomJS"
  wget --quiet -O /tmp/phantomjs.tar.bz2 https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
  tar -xjf /tmp/phantomjs.tar.bz2 -C /tmp
  mv /tmp/phantomjs-2.1.1-linux-x86_64/bin/phantomjs venv/bin/phantomjs
fi