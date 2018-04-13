
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
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

#
# REST configuration 
#
REST_API_TEST = True
