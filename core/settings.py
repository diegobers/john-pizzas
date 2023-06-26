import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ["SECRET_KEY_ENV_RAILWAY"]

DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'accounts.JohnPizzaAbstractUserModel'

LOGIN_REDIRECT_URL = 'index'

LOGIN_URL = 'login'

CSRF_ALLOWED_ORIGINS = ['https://john-pizzas-production.up.railway.app']

CSRF_TRUSTED_ORIGINS = ['https://john-pizzas-production.up.railway.app']

CORS_ORIGINS_WHITELIST = ['https://john-pizzas-production.up.railway.app']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my app's
    'orders',
    'accounts',
    'pages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
DATABASES = { 
    'default': dj_database_url.config(default=os.environ["DATABASE_URL"]),
}

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
LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = 'media/'
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AWS S3 Bucket with Boto3 and django-storages
AWS_ACCESS_KEY_ID = 'AKIA3COXWJFX6YQFBPRS'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'aws-s3djangoapps'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'