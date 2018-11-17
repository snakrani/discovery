
#-------------------------------------------------------------------------------
# Core Django settings

#
# Debugging
#
DEBUG = True
TEMPLATE_DEBUG = True

#
# Caching configuration
#
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'django_cache_table',
            'TIMEOUT': 300,
            'OPTIONS': {
                'MAX_ENTRIES': 50
            }
        }
    }

#-------------------------------------------------------------------------------
# Django Addons

#
# REST configuration 
#
REST_API_TEST = True
