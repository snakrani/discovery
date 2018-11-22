#!/usr/bin/env bash
# Test the Angular JS frontend application

set -e

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/../app"

TEST_ENGINE="${1:-karma}"

LOG_FILE="${2:-$SCRIPT_DIR/../logs/discovery-angular-${TEST_ENGINE}.log}"
if [ "$LOG_FILE" != "/dev/stdout" -a "$LOG_FILE" != "/dev/stderr" ]
then
  rm -f "$LOG_FILE"
fi

echo "> Testing Angular application (${TEST_ENGINE})" | tee -a "$LOG_FILE"
cd frontend

if [ "$TEST_ENGINE" == 'karma' ]
then
  ng test >>"$LOG_FILE" 2>&1
else
  ng "$TEST_ENGINE" >>"$LOG_FILE" 2>&1
fi