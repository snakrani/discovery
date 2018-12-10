#!/usr/bin/env bash
# Build the Angular JS frontend into a static app directory

set -e

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/../app"

LOG_FILE="${1:-$SCRIPT_DIR/../logs/discovery-angular-build.log}"
if [ "$LOG_FILE" != "/dev/stdout" -a "$LOG_FILE" != "/dev/stderr" ]
then
  rm -f "$LOG_FILE"
fi

TEMP_DIR=/tmp/frontend
FRONTEND_DIR="$SCRIPT_DIR/../app/frontend"

echo "> Building node modules" | tee -a "$LOG_FILE"

cd "$FRONTEND_DIR"
rm -Rf node_modules

if [ ! -z "$USER" -a "$USER" == 'vagrant' ]
then
  # This is needed to prevent build issues on Vagrant/Windows through
  # default Virtualbox directory sharing
  mkdir -p "$TEMP_DIR" >>"$LOG_FILE" 2>&1
  cp -f package.json "$TEMP_DIR" >>"$LOG_FILE" 2>&1
  cp -f package-lock.json "$TEMP_DIR" >>"$LOG_FILE" 2>&1
  
  cd "$TEMP_DIR"
  npm install >>"$LOG_FILE" 2>&1
  
  echo "> Copying node modules" | tee -a "$LOG_FILE"
  cp -Rf node_modules "$FRONTEND_DIR" >>"$LOG_FILE" 2>&1
  
  echo "> Copying package.lock" | tee -a "$LOG_FILE"
  cp -f package-lock.json "$FRONTEND_DIR" >>"$LOG_FILE" 2>&1
  cd "$FRONTEND_DIR"
else
  npm install >>"$LOG_FILE" 2>&1
fi

echo "> Building Angular files" | tee -a "$LOG_FILE"
ng build --prod --output-hashing none >>"$LOG_FILE" 2>&1

echo "> Fixing file permissions" | tee -a "$LOG_FILE"
find node_modules/.cache -type d -exec chmod 750 {} \; >>"$LOG_FILE" 2>&1
find node_modules/.cache -type f -exec chmod 640 {} \; >>"$LOG_FILE" 2>&1

