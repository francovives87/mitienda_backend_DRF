from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mitienda_app_2',
        'USER': 'mitienda_app_db_user',
        'PASSWORD': '@Gamefox33336078',
        'HOST': 'localhost',
        'PORT':'5432'
    }
}
##Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtpout.secureserver.net'
EMAIL_HOST_USER = 'contacto@mitienda.app'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = '@Gamefox33336078'
EMAIL_PORT = 80
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True

STATIC_URL = '/static/'
MEDIA_URL = '/media_root/'

STATICFILES_DIRS = [os.path.join( 'static')]
MEDIA_ROOT = os.path.join('media_root')
STATIC_ROOT = os.path.join('static_root')
