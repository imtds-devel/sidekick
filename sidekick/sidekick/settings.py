"""
Django settings for sidekick project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import configparser
import logging.config
from django.core.exceptions import ImproperlyConfigured


def require_env(name):
    # Raises an error if the environment variable isn't defined
    value = os.getenv(name)
    if value is None:
        raise ImproperlyConfigured('Required environment variable "{}" is not set.'.format(name))
    return value



# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

db_name = require_env('DB_NAME')
db_user = require_env('DB_USER')
db_password = require_env('DB_PASS')
db_host = require_env('DB_HOST')
db_port = require_env('DB_PORT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
        'HOST': db_host,
        'PORT': db_port
    }
}


# Google Cal Settings
ma = require_env('CAL_MA')
da = require_env('CAL_DA')
st = require_env('CAL_ST')
sd = require_env('CAL_SD')
rc = require_env('CAL_RC')
md = require_env('CAL_MD')
te = require_env('CAL_TE')

CALENDAR_LOCATION_IDS = {
    'ma': ma,
    'da': da,
    'st': st,
    'sd': sd,
    'rc': rc,
    'md': md,
    'te': te
}


# EMAIL SERVER
EMAIL_HOST = require_env('EMAIL_HOST')
EMAIL_PORT = require_env('EMAIL_PORT')
EMAIL_BUGADDR = require_env('EMAIL_BUGADDR')
EMAIL_SUBJECT_PREFIX = "[IMTDS]"

# HARMABOT
HARAMBOT_NOTIFY = os.getenv('HARAMBOT_NOTIFY')


debug = require_env('DEBUG') == "True"
PRODUCTION = require_env('PROD') == "True"


if PRODUCTION:
    print("Using SSL Encryption")
    SECURE_PROXY_SSL_HEADER = ('HTTPS_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    print("Using standard HTTP")
    SECURE_PROXY_SSL_HEADER = None
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = require_env('SECRET_KEY')

# Location of client_secret.json goes here
GOOGLE_OAUTH2_CLIENT_SECRETS_JSON = require_env('GOOGLE_CLIENT_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = debug

ALLOWED_HOSTS = [
    '192.168.8.33',
    'sidekick.devel.apu.edu',
    '127.0.0.1',
    '192.168.8.7',
    'sidekick.apu.edu',
]


# Application definition

INSTALLED_APPS = [
    'homebase.apps.HomebaseConfig',
    'passwords.apps.PasswordsConfig',
    'printinfo.apps.PrintinfoConfig',
    'quotes.apps.QuotesConfig',
    'roster.apps.RosterConfig',
    'shifts.apps.ShiftsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cas.apps.CASConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cas.middleware.CASMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sidekick.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sidekick.wsgi.application'


# Authentication
CAS_SERVER_URL = require_env('CAS_URL')
CAS_LOGOUT_COMPLETELY = True
CAS_PROVIDE_URL_TO_LOGOUT = True
CAS_FORCE_SSL_SERVICE_URL = False

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'cas.backends.CASBackend'
]

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = os.getenv('STATIC_URL')

if PRODUCTION:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
else:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static")
    ]


LOGGING_CONFIG = None
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'logfile': {
            'class': 'logging.FileHandler',
            'formatter': 'console',
            'filename': 'sk_log.log'
        },
        'email': {
            'class': 'logging.handlers.SMTPHandler',
            'formatter': 'console',
            'mailhost': (EMAIL_HOST, EMAIL_PORT),
            'fromaddr': 'bugmaster@sidekick.apu.edu',
            'toaddrs': [EMAIL_BUGADDR],
            'subject': 'Bug report!',
        }
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': ['console', 'logfile'],
        },
        'django': {
            'level': 'ERROR',
            'handlers': ['email']
        }
    },
})
