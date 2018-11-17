
#-------------------------------------------------------------------------------
# Core Django settings

#
# Debugging
#
DEBUG = True
TEMPLATE_DEBUG = False

#
# Database configurations
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

#-------------------------------------------------------------------------------
# Django Addons

#
# REST configuration 
#
REST_API_TEST = True
