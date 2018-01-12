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

config = configparser.ConfigParser()
config.read('config.ini')
db = config['database']
static_dir = config['static']
cal = config['cal_ids']
debug = config['prod']['debug'] == "True"
PRODUCTION = config['prod']['prod'] == "True"

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
SECRET_KEY = config['prod']['secret_key']

# Location of client_secret.json goes here
GOOGLE_OAUTH2_CLIENT_SECRETS_JSON = config['google']['client_secret']

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


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db['name'],
        'USER': db['user'],
        'PASSWORD': db['pass'],
        'HOST': db['host'],
        'PORT': db['port']
    }
}

# Authentication
CAS_SERVER_URL = config['cas']['url']
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

STATIC_URL = static_dir['url']

if PRODUCTION:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
else:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static")
    ]

# Google Cal Settings
CALENDAR_LOCATION_IDS = {
    'ma': cal['ma'],
    'da': cal['da'],
    'st': cal['st'],
    'sd': cal['sd'],
    'rc': cal['rc'],
    'md': cal['md'],
    'te': cal['te']
}

LOGGING = {

}
