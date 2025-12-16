from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {  # PostgreSQL (tienda)
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tienda_db',
        'USER': 'postgres',
        'PASSWORD': 'cami322',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },

    'mongodb': {  # MongoDB (API)
        'ENGINE': 'djongo',
        'NAME': 'zapatos_api',
        'HOST': 'localhost',
        'PORT': 27017,
    }
}

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
