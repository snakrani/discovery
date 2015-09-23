#!/bin/bash
waitress-serve --port=$VCAP_APP_PORT mirage.wsgi:application
