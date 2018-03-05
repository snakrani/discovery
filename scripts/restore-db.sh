#!/usr/bin/env bash
# Restore a Discovery database from a backup

set -e

DB_PORT=5432

SCRIPT_USAGE="
 Usage: <project-dir>/scripts/restore-db.sh [ -h ] <localname> [ <dbname> ]

   -h | --help                |  Display this help message
   -p | --port                |  PostgreSQL port to connect to (default $DB_PORT) 
   -u | --user                |  Database username to connect with (default <dbname>)
"

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

source "$SCRIPT_DIR/bash-opts.sh"
source "$SCRIPT_DIR/bash-validators.sh"

#-------------------------------------------------------------------------------
# Argument / Options

PARAMS=`normalize_params "$@"`

parse_flag '-h|--help' HELP_WANTED

if [ "$HELP_WANTED" ]
then
  echo "$SCRIPT_USAGE"
  exit 0
fi

parse_option '-p|--port' DB_PORT validate_string "PostgreSQL port can not be empty if option used" || exit 4
parse_option '-u|--user' DB_USER validate_string "PostgreSQL username can not be empty if option used" || exit 5

ARGS=(`get_args "$PARAMS"`)

LOCAL_NAME="${ARGS[0]}"
DB_NAME="${ARGS[1]}"

#-------------------------------------------------------------------------------
# Validation

if [ -z "$LOCAL_NAME" ]
then
  echo "Local database file name is required as first argument.  See --help for more information."
  exit 6  
fi
if [ -z "$DB_NAME" ]
then
  DB_NAME="$LOCAL_NAME"
fi
if [ -z "$DB_USER" ]
then
  DB_USER="$DB_NAME"
fi

#-------------------------------------------------------------------------------
# Execution

echo "
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
" > /tmp/db.sql

cat "db/${LOCAL_NAME}.sql" >> /tmp/db.sql

psql "$DB_NAME" --host=localhost --port="$DB_PORT" --username="$DB_USER" --password < /tmp/db.sql
rm /tmp/db.sql
