
#
# General project variables
#
DEBUG = False
TEMPLATE_DEBUG = False

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

#
# REST configuration 
#
REST_API_TEST = True
