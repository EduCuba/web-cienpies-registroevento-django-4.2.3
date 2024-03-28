"""
Django settings for registroevento project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import pymysql
#Agregado para conectar a base remoto desde app local
import dj_database_url
#agregado para render
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(hdas)*9g)plrw1$8n6m$^6l))qxu)z#s(54bn#mgn1mc5tpa)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]
#ALLOWED_HOSTS = ['3.80.73.116','localhost', '127.0.0.1']
#ALLOWED_HOSTS = ['acreditacion.pythonanywhere.com','localhost', '127.0.0.1']

#i-0e58ae49ce9e01355
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'bases',
    'eve',
    'par',
    'django_userforeignkey',
    'django.contrib.postgres',
    'registroevento',
]

#MIDDLEWARE = [
#    'django.middleware.security.SecurityMiddleware',
#    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.messages.middleware.MessageMiddleware',
#    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'django_userforeignkey.middleware.UserForeignKeyMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware'
#]

#Agregado para Render en el manejo de static
#'whitenoise.middleware.WhiteNoiseMiddleware',
MIDDLEWARE = [
     
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
   
    'django_userforeignkey.middleware.UserForeignKeyMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]





ROOT_URLCONF = 'registroevento.urls'

#'DIRS': [],
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'registroevento.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

#Conexion a servidor RENDER
#postgres://db_registro_user:IucxPCOSyWJgoqeOOo1hhzuDn4JAHX5c@dpg-cntgp1sf7o1s73f43iu0-a.oregon-postgres.render.com/db_registro


#db_config = dj_database_url.config(default='')
#db_config = dj_database_url.parse(default='postgres://db_registro_user:IucxPCOSyWJgoqeOOo1hhzuDn4JAHX5c@dpg-cntgp1sf7o1s73f43iu0-a.oregon-postgres.render.com/db_registro')
#URL Externa
#db_config = dj_database_url.parse('postgres://db_registro_user:IucxPCOSyWJgoqeOOo1hhzuDn4JAHX5c@dpg-cntgp1sf7o1s73f43iu0-a.oregon-postgres.render.com/db_registro')
#URL Interna
db_config = dj_database_url.parse('postgres://db_registro_user:IucxPCOSyWJgoqeOOo1hhzuDn4JAHX5c@dpg-cntgp1sf7o1s73f43iu0-a/db_registro')
#db_config['ATOMIC_REQUESTS'] = True
DATABASES = {
    'default': db_config,
}

#Local Host PostgreSql
#'ENGINE': 'django.db.backends.postgresql_psycopg2',
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'db_registro',
#        'HOST': 'localhost',
#        'USER': 'postgres',
#        'PASSWORD': 'postgresql',
#        'PORT': 5432,
#    }
#}

#'HOST':'registro-db.cmpbm7wydymj.us-east-1.rds.amazonaws.com',
#'HOST': 'localhost',
         
#Mysql

#DATABASES = {
#  'default': {
#      'ENGINE': "django.db.backends.mysql",
#      'NAME': "acreditacion$db_registro",
#      'USER': "acreditacion",
#      'PASSWORD': "mYpt#35uk%Yo",
#      'HOST': "acreditacion.mysql.pythonanywhere-services.com",
#      'PORT': "3306",
#    }
#}
# Remoto :
#'NAME': "acreditacion$db_registro",
#'USER': "acreditacion",
#'HOST': "acreditacion.mysql.pythonanywhere-services.com",
#'HOST': "acreditacion.mysql.pythonanywhere-services.com",

#Local :
#'NAME': "db_registro",
#'USER': "root",
#'HOST': 'localhost',

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
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'es-pe'
#TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

#Agregado para Render
#Esto combina la compresión automática con el comportamiento de almacenamiento en caché proporcionado por Backend ManifestStaticFilesStorage de Django. Si desea aplicar compresión pero no desea el comportamiento de almacenamiento en caché, puede usar el backend alternativo:
#"whitenoise.storage.CompressedStaticFilesStorage"
#STORAGES = {
    # ...
 #   "staticfiles": {
 #       "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
 #   },
#}


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    '/var/www/static/'
]

# This production code might break development mode, so we check whether we're in DEBUG mode
if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

#MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_ROOT = {BASE_DIR /'media'}
MEDIA_URL = '/media/'

#LOGIN_REDIRECT_URL = '/'
#LOGOUT_REDIRECT_URL = '/login/'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#seteamos para que trabaje con la tabla usuario
AUTH_USER_MODEL = 'bases.Usuario'


INTERNAL_IPS = [
    "127.0.0.1", 
]


