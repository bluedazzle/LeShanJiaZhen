"""
Django settings for homemaking project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '89_#q=qbk+udde-*1t-e*y^mx9kokruzv5(g##stsdlmh*d^_@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin_area',
    'admin_all',
    'HomeApi',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'homemaking.urls'

WSGI_APPLICATION = 'homemaking.wsgi.application'

SESSION_ENGINE = "django.contrib.sessions.backends.file"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DB_ENGINE = 'django.db.backends.postgresql_psycopg2'
DB_NAME = 'LSHM'
DB_USER = 'postgres'                      # Not used with sqlite3.
DB_PASSWORD = 'GDBDYL886'                  # Not used with sqlite3.
DB_HOST = 'localhost'                      # Set to empty string for localhost. Not used with sqlite3.
DB_PORT = '5433'

DATABASES = {
    'default': {
        'ENGINE':   DB_ENGINE,
        'NAME':     DB_NAME,
        'USER':     DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST':     DB_HOST,
        'PORT':     DB_PORT,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'utf-8'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

APPEND_SLASH = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

CSS_DIR = './static/css/'
IMG_DIR = './static/img/'
UP_DIR = './upload/'
JS_DIR = './static/js/'
FILE_DIR = './static/file/'
FONTS_DIR = './static/fonts/'
OUT_FILES_DIR ='./out_files/'
APK_DIR = './static/apk/'
