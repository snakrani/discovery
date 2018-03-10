"""
Django settings for the Discovery project.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
from discovery.utils import config_value

import os
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
API_CACHE_LIFETIME = 24 # in hours

API_HOST = config_value('API_HOST', '')

SAM_API_URL = "https://api.data.gov/sam/v1/registrations/"
SAM_API_KEY = config_value('SAM_API_KEY', '')

#
# Discovery related settings
#
VEHICLES = (
    'oasis_sb', 
    'oasis', 
    'hcats_sb', 
    'hcats',
    'bmo_sb',
    'bmo'
)

#-------------------------------------------------------------------------------
# Core Django settings

#
# Debugging
#
DEBUG = False
TEMPLATE_DEBUG = False

#
# General configurations
#
SECRET_KEY = config_value('SECRET_KEY', '')
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
    'discovery',
    'api',
    'categories',
    'vendors',
    'contracts',
    
    'tests',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'db_mutex',
    
    'rest_framework',
    'django_filters',
    'rest_framework_filters',
    'crispy_forms',
    
    'django_celery_beat',
    'django_celery_results'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware'
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
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
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
        'django.template': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'INFO',
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
# REST configuration 
#
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'api.schemas.DiscoverySchema',
    
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    
    'DEFAULT_FILTER_BACKENDS': [],
    'SEARCH_PARAM': 'q',
    
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    
    'COERCE_DECIMAL_TO_STRING': False,
}

#-------------------------------------------------------------------------------
#
# Local settings overrides
#
try:
    from discovery.local_settings import *
except:
    pass
