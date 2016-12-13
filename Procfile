web: python manage.py migrate --noinput && python manage.py createcachetable && waitress-serve --expose-tracebacks --port=$PORT mirage.wsgi:application
