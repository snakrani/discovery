DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'circle_test',
        'USER': 'ubuntu',
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
