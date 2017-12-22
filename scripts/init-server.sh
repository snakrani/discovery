#!/usr/bin/env bash
# Prepare a python enabled server for application hosting.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

#activate the virtual python environment
source venv/bin/activate

#run application setup commands

echo "> Migrating Django database structure"
./manage.py migrate --noinput > /dev/null

echo "> Ensuring Django cache table"
./manage.py createcachetable > /dev/null

echo "> Collecting Django static files"
./manage.py collectstatic --noinput > /dev/null

echo "> Loading basic category information"
./manage.py load_categories > /dev/null
