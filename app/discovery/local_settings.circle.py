
#
# General project variables
#
DEBUG = True
TEMPLATE_DEBUG = True


#
# Database connections
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'circle-test',
        'USER': 'circleci',
        'PASSWORD': 'circleci'
    }
}
