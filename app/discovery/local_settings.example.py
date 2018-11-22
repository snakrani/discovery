
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
    PAGE_CACHE_LIFETIME = 30 # seconds
    
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        },
        'page_cache': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'django_cachepage',
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
