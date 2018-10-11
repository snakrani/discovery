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

echo "> Building Angular files" | tee -a "$LOG_FILE"
cd frontend
ng build --prod >>"$LOG_FILE" 2>&1
