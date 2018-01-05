"""
Django settings for the Discovery project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
from discovery_site.cloud import cloud_config

import os
import markdown
import dj_database_url

#
# General project variables
#
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Django specific
#------------------------------

SECRET_KEY = cloud_config('SECRET_KEY', '')
APPEND_SLASH = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

DB_MUTEX_TTL_SECONDS = 86400 # 1 day (24 hours)

# Application specific
#------------------------------

API_HOST = cloud_config('API_HOST', '')
API_KEY = cloud_config('API_KEY', '')

SAM_API_URL = "https://api.data.gov/sam/v1/registrations/"
SAM_API_KEY = cloud_config('SAM_API_KEY', '')

VEHICLES = ('oasissb', 'oasis')


#
# Application definitiona and scope
#
WSGI_APPLICATION = 'discovery.wsgi.application'
ROOT_URLCONF = 'discovery.urls'

ALLOWED_HOSTS = [
    '*',
]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'db_mutex',
    'storages',
    'selenium_tests',
    'rest_framework',
    'rest_framework_swagger',
    'django_celery_beat',
    'django_celery_results',

    'api',
    'discovery_site',
    'vendors',
    'contract',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "discovery.context_processors.api_host",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.request',
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'discovery_site/templates'),
)


#
# Time and internationalization
#
TIME_ZONE = 'UTC'
USE_TZ = True

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True


#
# Database connections
#
DATABASES = {}
DATABASES['default'] = dj_database_url.config()


#
# Static file handling
#
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#The below settings turn on S3 bucket storage
#Lines below are commented out to force the loading of static assets from the local dev server by default
#uncomment them and fill in the extra AWS settings to hook it up to an S3 bucket

#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = cloud_config('AWS_ACCESS_KEY_ID', '')

AWS_SECRET_ACCESS_KEY = cloud_config('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = cloud_config('AWS_STORAGE_BUCKET_NAME', '')


#
# Application logging
#
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache_table',
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'csv': {
            'format' : '"%(asctime)s","%(levelname)s",%(message)s',
            'datefmt' : "%Y-%m-%d %H:%M:%S"
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/discovery.log'),
            'formatter': 'verbose'
        },
        'vendor_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/vendor.log'),
            'formatter': 'verbose'
        },
        'vendor_memory_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/vendor_memory.csv'),
            'formatter': 'csv'
        },
        'vendor_data_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/vendor_data.csv'),
            'formatter': 'csv'
        },
        'sam_data_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/sam_data.csv'),
            'formatter': 'csv'
        },
        'fpds_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/fpds.log'),
            'formatter': 'verbose'
        },
        'fpds_memory_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/fpds_memory.csv'),
            'formatter': 'csv'
        },
        'fpds_data_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/fpds_data.csv'),
            'formatter': 'csv'
        }
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG'
        },
        'vendor': {
            'handlers': ['vendor_file'],
            'level': 'DEBUG'
        },
        'vendor_memory': {
            'handlers': ['vendor_memory_file'],
            'level': 'INFO'
        },
        'vendor_data': {
            'handlers': ['vendor_data_file'],
            'level': 'INFO'
        },
        'sam_data': {
            'handlers': ['sam_data_file'],
            'level': 'INFO'
        },
        'fpds': {
            'handlers': ['fpds_file'],
            'level': 'DEBUG'
        },
        'fpds_memory': {
            'handlers': ['fpds_memory_file'],
            'level': 'INFO'
        },
        'fpds_data': {
            'handlers': ['fpds_data_file'],
            'level': 'INFO'
        }
    },
}


#
# Administrative session handling
#
SESSION_ENGINE = 'redis_sessions.session'

SESSION_REDIS = {
    'host': cloud_config('hostname', 'localhost', ['redis28', 'redis32'], 'discovery-auth'),
    'port': cloud_config('port', '6379', ['redis28', 'redis32'], 'discovery-auth'),
    'db': 0,
    'password': cloud_config('password', 'discovery', ['redis28', 'redis32'], 'discovery-auth'),
    'prefix': 'session',
    'socket_timeout': 1
}


#
# Celery processing and scheduling
#
CELERY_BROKER_URL = cloud_config('uri', 'redis://:discovery@localhost:6379', ['redis28', 'redis32'], 'discovery-tasks')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


#
# Saucelabs testing
#
SAUCE = False
SAUCE_USERNAME = cloud_config('SAUCE_USERNAME', '')
SAUCE_ACCESS_KEY = cloud_config('SAUCE_ACCESS_KEY', '')
DOMAIN_TO_TEST = cloud_config('SAUCE_DOMAIN', 'domain.of.your.discovery.installation.gov')


#
#  Swagger documentation configuration
#
SWAGGER_SETTINGS = {
    "doc_expansion": "full",
    "exclude_namespaces": [], # List URL namespaces to ignore
    "api_version": '0.1',  # Specify your API's version
    "api_path": "/",  # Specify the path to your API not a root level
    "api_host": '', #comment out until fix swagger - API_HOST, #the data.gov api host
    "enabled_methods": [  # Specify which methods to enable in Swagger UI
        'get',
    ],
    "api_key": '', #Acomment out until fix swagger PI_KEY , # An API key
    "is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": False,  # Set to True to enforce admin only access
    "permission_denied_handler": None, # If user has no permisssion, raise 403 error
    "info": {
        "contact": "discovery-18f@gsa.gov",
        "title": "Discovery Market Research API",
        "description": markdown.markdown("""
This API drives the [Discovery Market Research Tool](https://discovery.gsa.gov).
It contains information on the vendors that are part of the OASIS and OASIS Small Business contracting vehicles, such as their contracting history, their elligibility for contract awards, and their small business designations.
To learn more about the tool, please visit [Discovery](https://discovery.gsa.gov) or see the README on our [GitHub repository](https://github.com/PSHCDevOps/discovery).

**Please note that the base path for this API is `https://api.data.gov/gsa/discovery/`**

It requires an API key, obtainable at [api.data.gov](http://api.data.gov/).
It must be passed in the `api_key` parameter with each request.
        """), #converts markdown description to HTML
    },
    "template_path": "api_theme/index.html",
}


# Optionally override any configurations above
try:
    from discovery.local_settings import *
except:
    pass
