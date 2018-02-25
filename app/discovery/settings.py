"""
Django settings for the Discovery project.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
from discovery.utils import config_value

import os
import markdown
import dj_database_url

#-------------------------------------------------------------------------------
# Global settings

#
# Directories
#
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ_DIR = os.path.dirname(BASE_DIR)

#
# API settings
#
API_HOST = config_value('API_HOST', '')
API_KEY = config_value('API_KEY', '')

SAM_API_URL = "https://api.data.gov/sam/v1/registrations/"
SAM_API_KEY = config_value('SAM_API_KEY', '')

#
# Discovery related settings
#
VEHICLES = (
    'oasis_sb', 
    'oasis', 
    'hcats_sb', 
    'hcats'
)

#-------------------------------------------------------------------------------
# Core Django settings

#
# Debugging
#
DEBUG = True
TEMPLATE_DEBUG = True

#
# General configurations
#
SECRET_KEY = '123456789' #config_value('SECRET_KEY', '')
APPEND_SLASH = True

#
# Time configuration
#
TIME_ZONE = 'UTC'
USE_TZ = True

#
# Language configurations
#
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

#
# Server configurations
#
WSGI_APPLICATION = 'discovery.wsgi.application'
ROOT_URLCONF = 'discovery.urls'

ALLOWED_HOSTS = [
    '*',
]

#
# Database configurations
#
DATABASES = {}
DATABASES['default'] = dj_database_url.config()

#
# Applications and libraries
#
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'db_mutex',
    'storages',
    
    'rest_framework',
    'rest_framework_swagger',
    
    'django_celery_beat',
    'django_celery_results',

    'discovery',
    'api',
    'categories',
    'vendors',
    'contracts',
    
    'tests',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#
# Authentication configuration
#
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#
# Templating configuration
#
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.core.context_processors.auth',
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'discovery.context_processors.api_host',
            ],
        },
    },
]

#
# Static file configurations
#
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#
# Caching configuration
#
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache_table',
    }
}

#
# Logging configuration
#
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
            'filename': os.path.join(PROJ_DIR, 'logs/discovery.log'),
            'formatter': 'verbose'
        },
        'vendor_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJ_DIR, 'logs/vendor.log'),
            'formatter': 'verbose'
        },
        'vendor_memory_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJ_DIR, 'logs/vendor_memory.csv'),
            'formatter': 'csv'
        },
        'vendor_data_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJ_DIR, 'logs/vendor_data.csv'),
            'formatter': 'csv'
        },
        'sam_data_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJ_DIR, 'logs/sam_data.csv'),
            'formatter': 'csv'
        },
        'fpds_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJ_DIR, 'logs/fpds.log'),
            'formatter': 'verbose'
        },
        'fpds_memory_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJ_DIR, 'logs/fpds_memory.csv'),
            'formatter': 'csv'
        },
        'fpds_data_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJ_DIR, 'logs/fpds_data.csv'),
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

#-------------------------------------------------------------------------------
# Django Addons

#
# Mutex locking configuration
#
DB_MUTEX_TTL_SECONDS = 86400 # 1 day (24 hours)

#
# Administrative session handling
#
SESSION_ENGINE = 'redis_sessions.session'

SESSION_REDIS = {
    'host': config_value('hostname', 'localhost', ['redis28', 'redis32'], 'discovery-auth'),
    'port': config_value('port', '6379', ['redis28', 'redis32'], 'discovery-auth'),
    'db': 0,
    'password': config_value('password', 'discovery', ['redis28', 'redis32'], 'discovery-auth'),
    'prefix': 'session',
    'socket_timeout': 1
}

#
# Celery processing and scheduling
#
CELERY_BROKER_URL = config_value('uri', 'redis://:discovery@localhost:6379', ['redis28', 'redis32'], 'discovery-tasks')
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
SAUCE_USERNAME = config_value('SAUCE_USERNAME', '')
SAUCE_ACCESS_KEY = config_value('SAUCE_ACCESS_KEY', '')
DOMAIN_TO_TEST = config_value('SAUCE_DOMAIN', 'domain.of.your.discovery.installation.gov')


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

#-------------------------------------------------------------------------------
#
# Local settings overrides
#
try:
    from discovery.local_settings import *
except:
    pass
