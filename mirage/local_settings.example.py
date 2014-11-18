DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'oasis',
        'USER': 'oasis',
        'PASSWORD': ''
    }
}

SAM_API_KEY = ''

# SECURITY WARNING: keep the secret key used in production secret!
# change this before deploying to your own server!
SECRET_KEY = '&%7l9-fvi7_9ykzb*kr1bhjfx%x=(vd0r8z4w#p154eb1o+t=o'

SAUCE = False
SAUCE_USERNAME = ''
SAUCE_ACCESS_KEY = ''
DOMAIN_TO_TEST = 'domain.of.your.mirage.installation.gov'


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#S3_URL = 'https://s3-us-west-2.amazonaws.com/mirage.gsa.gov/'

AWS_ACCESS_KEY_ID = ''
AWS_QUERYSTRING_AUTH = False
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''

