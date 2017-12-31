#!/usr/bin/env bash
# "SSH" into a container in the discovery cluster
#
# TODO: Support both docker and cf "ssh" wrappers
#

SCRIPT_USAGE="
 Usage: <project-dir>/scripts/ssh.sh [ -hd ] [ <container-name> ]

   -d | --docker   |  Name refers to the base docker name for the container (default: docker-compose name)
   -n | --network  |  Name of the Docker Compose network (default: vagrant)
   -i | --instance |  Instance number of the Docker Compose container (default: 1)
   -h | --help     |  Display this help message
"

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

#-------------------------------------------------------------------------------
# Defaults

DEFAULT_CONTAINER_NAME="web"

NETWORK_NAME="vagrant"
INSTANCE_NUM="1"

#-------------------------------------------------------------------------------
# Option / Argument parsing

SCRIPT_ARGS=()
FORCE_CREATE=''

while [[ $# > 0 ]]
do
  key="$1"

  case $key in
    -h|--help)
      echo "$SCRIPT_USAGE"
      exit 0
    ;;
    -n|--network)
      NETWORK_NAME="$2"
      shift
    ;;
    -i|--instance)
      INSTANCE_NUM="$2"
      shift
    ;;
    -d|--docker)
      BASE_DOCKER_NAME='true'
    ;;
    *)
      # argument
      SCRIPT_ARGS+=("$key")
    ;;
  esac
  shift
done

CONTAINER_NAME="${SCRIPT_ARGS[0]}"

if [ -z "$CONTAINER_NAME" ]
then
  CONTAINER_NAME="$DEFAULT_CONTAINER_NAME"
fi

if [ -z "$BASE_DOCKER_NAME" ]
then
  # Docker Compose prefixes network and suffixes instance number
  CONTAINER_NAME="${NETWORK_NAME}_${CONTAINER_NAME}_${INSTANCE_NUM}"
fi

#-------------------------------------------------------------------------------
# Execution

docker exec -it $CONTAINER_NAME bash
