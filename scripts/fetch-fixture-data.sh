#!/usr/bin/env bash
# Fetch site data from remote sources (just enough to generate effective fixtures)
#

set -e

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/../app"

./manage.py parse_categories
./manage.py load_vendors --vpp=10
./manage.py load_sam --tries=3 --pause=1
./manage.py load_fpds --reinit --starting_date='2008-02-22' --load=520 --count=10 --max=10 --pause=1
