"""
Django settings for scs project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
MAINTENANCE_MODE = False
ALLOWED_HOSTS = ['stickycatstickers.in','localhost','127.0.0.1','34.131.80.185','www.stickycatstickers.in']
AUTH_USER_MODEL = 'accounts.CustomUser'


# Application definition

INSTALLED_APPS = [
    'maintenance_mode',
    'shop.apps.ShopConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'django_filters',
    
    
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
]

ROOT_URLCONF = 'scs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'scs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    "accounts/static",
] 

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#managing media
MEDIA_ROOT = Path(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtpout.secureserver.net'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'support@stickycatstickers.in'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True


#phonepe
MERCH_ID = os.environ.get('MERCH_ID')
MERCH_SALT = os.environ.get('MERCH_SALT')

#shiprocket
SHIPROCKET_TOKEN = os.environ.get('SHIPROCKET_TOKEN')

#CSRF_COOKIE_SECURE = True #to avoid transmitting the CSRF cookie over HTTP accidentally.
#SESSION_COOKIE_SECURE = True #to avoid transmitting the session cookie over HTTP accidentally.

# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True

# SECURE_SSL_REDIRECT = True

# SECURE_HSTS_SECONDS = 86400  # 1 day
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True


