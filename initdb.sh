#!/bin/bash
waitress-serve --port=$PORT mirage.wsgi:application
