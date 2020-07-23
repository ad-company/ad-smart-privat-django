"""
Django settings for adsmartprivat project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rfykm3pwi6n#&r2l#qxv)=z3%j_4$y@8f-dnn#1d0+l_m2xc7m'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False

ALLOWED_HOSTS = [
    '0.0.0.0',
    'ad-smart-privat.herokuapp.com',
    'adsmartprivat.herokuapp.com'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'json_field', # Handle model JSON
    # 'psycopg2', # PostgreSQL handler
    'home',
    'main_absence_schedule',
    'main_register_tentor',
    'main_register_student',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django_cookies_samesite.middleware.CookiesSameSite',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'adsmartprivat.middleware.SettingsMiddleware'  ## Custom Middleware
]

ROOT_URLCONF = 'adsmartprivat.urls'

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

WSGI_APPLICATION = 'adsmartprivat.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

## MYSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'ad-smart-privat-django',
        'USER': 'root',
        'PASSWORD': 'warcr4ft',
        'HOST': '0.0.0.0',
        'PORT': '3306',
    }
}

# DATABASES = {
#     ## POSTGRESQL
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": "adsmartprivatdjango",
#         "USER": "aswindanu",
#         "PASSWORD": "",
#         "HOST": "0.0.0.0",
#         "PORT": "5432",
#     },

#     # Mongo
#     "mongodb": {
#       "ENGINE": "djongo",
#       "NAME": "adsmartprivat-mongo",
#    }
# }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# Sackoverview docs : https://stackoverflow.com/questions/5517950/django-media-url-and-media-root
PROJECT_ROOT   =   os.path.join(os.path.abspath(__file__))
if not DEBUG:
    STATIC_ROOT  =   os.path.join(BASE_DIR, 'uploads/static')  ## for manage.py collecstatic
    # Extra lookup directories for collectstatic to find static files
    STATICFILES_DIRS = (
        os.path.join(PROJECT_ROOT, '../../uploads/static/static'),
    )
STATIC_URL = '/static/' ## endpoint direct to static example: 0.0.0.0:3000/static/css/home.css

MEDIA_URL = '/media/' ## endpoint direct to upload file example: 0.0.0.0:3000/media/uploads/...
MEDIA_ROOT = (
    ## in Root project, ex: ad-smart-privat-django
    os.path.join(BASE_DIR)
)

if DEBUG:
    STATIC_ROOT  =   os.path.join(BASE_DIR, 'uploads/static/static')  ## for manage.py collecstatic
    # Extra lookup directories for collectstatic to find static files
    STATICFILES_DIRS = (
        os.path.join(PROJECT_ROOT, '../../uploads/static'),
    )

#  Add configuration for static files storage using whitenoise
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ===== A&D Custom =====
# solve MYSQL
import pymysql
pymysql.install_as_MySQLdb()

SESSION_COOKIE_SAMESITE_KEYS = {'my-custom-cookies'}
# or
DCS_SESSION_COOKIE_SAMESITE_KEYS = {'my-custom-cookies'}

SESSION_COOKIE_SAMESITE_FORCE_ALL = True
# or
DCS_SESSION_COOKIE_SAMESITE_FORCE_ALL = True

# SSL
# PREPEND_WWW = True
# BASE_URL = "https://adsmartprivat.herokuapp.com"
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# ===

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        'file': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
        },
    },
    'loggers': {
        # root logger
        '': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# Login URL
LOGIN_URL='/login'
LOGOUT_URL='/logout'
LOGIN_REDIRECT_URL='/'
LOGOUT_REDIRECT_URL='/'

# Recaptcha
GOOGLE_RECAPTCHA_SECRET_KEY = '6LcnsaMZAAAAAAbDwd5W4ITWbX3XLKuq8zCdm1Lt'

# Heroku
import dj_database_url 
prod_db  =  dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)
# ==================
