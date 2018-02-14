#!/usr/bin/env bash
# Fetch site data from remote sources (just enough to generate effective fixtures)
#

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/../app"

./manage.py load_categories
./manage.py load_vendors --vpp=0 --tries=3 --pause=1
./manage.py load_fpds --reinit --starting_date='2008-02-22' --load=520 --count=50 --max=50 --pause=1
./manage.py load_fpds --id=135 --starting_date='2008-02-22' --load=520 --count=500 --max=500 --pause=1
