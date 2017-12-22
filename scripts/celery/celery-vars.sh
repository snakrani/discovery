
CELERYD_NODES="worker1"
CELERYD_NODES=1

PATH="${PATH:+$PATH:}/usr/sbin:/sbin:/vagrant/venv/bin"
CELERY_BIN="/vagrant/venv/bin/celery"

CELERY_APP="discovery"
CELERYD_CHDIR="/vagrant"

CELERYD_OPTS="--time-limit=300 --concurrency=2"

CELERYD_LOG_LEVEL="INFO"
CELERYD_LOG_FILE="/vagrant/logs/celery/%N.log"
CELERYD_PID_FILE="/var/run/celery/%N.pid"

CELERYD_USER="vagrant"
CELERYD_GROUP="vagrant"

CELERY_CREATE_DIRS=1
