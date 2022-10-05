from .base import *
from home_vote.settings import base

DEBUG = False

ALLOWED_HOSTS = ['emale-meals.herokuapp.com']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE'),
        'USER': os.getenv('USER'),
        'PASSWORD': os.getenv('PASSWORD'),
        'HOST': os.getenv('HOST'),
        'PORT': '5432',
    }
}

MIDDLEWARE = base.MIDDLEWARE + [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

INSTALLED_APPS = base.INSTALLED_APPS + [
    'whitenoise.runserver_nostatic',
]