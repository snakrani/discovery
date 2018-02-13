
#
# General project variables
#
DEBUG = True
TEMPLATE_DEBUG = True

SAUCE = False

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
    