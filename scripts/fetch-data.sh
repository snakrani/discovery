#!/usr/bin/env bash
# Fetch site data from remote sources
#
# > For faster fixture data, run: scripts/load-fixtures.sh
#

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/../app"

# TODO: Set vpp, period, max, and pause from options

./manage.py parse_categories
./manage.py load_vendors --vpp=0
./manage.py load_sam --tries=3 --pause=1
./manage.py load_fpds --reinit --period=520 --load=52 --count=500 --max=0 --pause=1
