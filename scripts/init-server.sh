#!/usr/bin/env bash
python manage.py migrate --noinput
python manage.py createcachetable
python manage.py collectstatic --noinput
python manage.py load_categories
