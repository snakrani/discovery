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

cd frontend


echo "> Building node modules" | tee -a "$LOG_FILE"
rm -Rf node_modules
npm install >>"$LOG_FILE" 2>&1

echo "> Building Angular files" | tee -a "$LOG_FILE"
ng build --prod >>"$LOG_FILE" 2>&1

echo "> Fixing file permissions" | tee -a "$LOG_FILE"
find node_modules/.cache -type d -exec chmod 750 {} \; >>"$LOG_FILE" 2>&1
find node_modules/.cache -type f -exec chmod 640 {} \; >>"$LOG_FILE" 2>&1
